from __future__ import annotations

import json
from datetime import date, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from clinic_booking.service import AppointmentService, default_doctors

service = AppointmentService(default_doctors())


class AppointmentHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/doctors":
            self._send_json(
                200,
                [
                    {
                        "id": doctor.id,
                        "name": doctor.name,
                        "work_start": doctor.work_start.strftime("%H:%M"),
                        "work_end": doctor.work_end.strftime("%H:%M"),
                    }
                    for doctor in service.doctors
                ],
            )
            return

        if parsed.path.startswith("/doctors/") and parsed.path.endswith("/slots"):
            parts = parsed.path.strip("/").split("/")
            if len(parts) != 3:
                self._send_json(404, {"error": "not found"})
                return

            doctor_id = parts[1]
            params = parse_qs(parsed.query)
            day_str = params.get("date", [None])[0]
            if not day_str:
                self._send_json(400, {"error": "date query parameter is required"})
                return

            try:
                day = date.fromisoformat(day_str)
                slots = service.list_free_slots(doctor_id, day)
            except ValueError as exc:
                self._send_json(400, {"error": str(exc)})
                return

            self._send_json(200, {"doctor_id": doctor_id, "date": day_str, "free_slots": [slot.strftime("%H:%M") for slot in slots]})
            return

        self._send_json(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/appointments":
            self._send_json(404, {"error": "not found"})
            return

        payload = self._read_json_body()
        if payload is None:
            return

        required = {"doctor_id", "date", "start_time", "patient_id"}
        if not required.issubset(payload):
            self._send_json(400, {"error": "doctor_id, date, start_time and patient_id are required"})
            return

        try:
            appointment = service.book_slot(
                doctor_id=str(payload["doctor_id"]),
                day=date.fromisoformat(str(payload["date"])),
                start=time.fromisoformat(str(payload["start_time"])),
                patient_id=str(payload["patient_id"]),
            )
        except ValueError as exc:
            self._send_json(409 if str(exc) == "slot already booked" else 400, {"error": str(exc)})
            return

        self._send_json(
            201,
            {
                "id": appointment.id,
                "doctor_id": appointment.doctor_id,
                "patient_id": appointment.patient_id,
                "date": appointment.day.isoformat(),
                "start_time": appointment.start.strftime("%H:%M"),
                "end_time": appointment.end.strftime("%H:%M"),
            },
        )

    def do_DELETE(self) -> None:  # noqa: N802
        if not self.path.startswith("/appointments/"):
            self._send_json(404, {"error": "not found"})
            return

        appointment_id = self.path.rsplit("/", 1)[-1]
        if not appointment_id.isdigit():
            self._send_json(400, {"error": "invalid appointment id"})
            return

        cancelled = service.cancel_appointment(int(appointment_id))
        if not cancelled:
            self._send_json(404, {"error": "appointment not found"})
            return

        self._send_json(200, {"status": "cancelled"})

    def _read_json_body(self):
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(content_length)
            return json.loads(body.decode("utf-8"))
        except (ValueError, json.JSONDecodeError):
            self._send_json(400, {"error": "invalid JSON payload"})
            return None

    def _send_json(self, status: int, payload) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run() -> None:
    server = ThreadingHTTPServer(("0.0.0.0", 8000), AppointmentHandler)
    print("Serving appointment API on http://0.0.0.0:8000")
    server.serve_forever()


if __name__ == "__main__":
    run()
