from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from itertools import count
from threading import Lock
from typing import Dict, List

SLOT_MINUTES = 30


@dataclass(frozen=True)
class Doctor:
    id: str
    name: str
    work_start: time
    work_end: time


@dataclass(frozen=True)
class Appointment:
    id: int
    doctor_id: str
    patient_id: str
    day: date
    start: time
    end: time


class AppointmentService:
    def __init__(self, doctors: List[Doctor]):
        self._doctors: Dict[str, Doctor] = {doctor.id: doctor for doctor in doctors}
        self._appointments: Dict[int, Appointment] = {}
        self._id_sequence = count(1)
        self._lock = Lock()

    @property
    def doctors(self) -> List[Doctor]:
        return list(self._doctors.values())

    def list_free_slots(self, doctor_id: str, day: date) -> List[time]:
        doctor = self._get_doctor(doctor_id)
        booked_starts = {
            appt.start
            for appt in self._appointments.values()
            if appt.doctor_id == doctor_id and appt.day == day
        }

        slots: List[time] = []
        current = datetime.combine(day, doctor.work_start)
        end = datetime.combine(day, doctor.work_end)
        step = timedelta(minutes=SLOT_MINUTES)
        while current + step <= end:
            if current.time() not in booked_starts:
                slots.append(current.time())
            current += step
        return slots

    def book_slot(self, doctor_id: str, day: date, start: time, patient_id: str) -> Appointment:
        doctor = self._get_doctor(doctor_id)
        self._validate_slot_bounds(doctor, start)
        end = (datetime.combine(day, start) + timedelta(minutes=SLOT_MINUTES)).time()

        with self._lock:
            for appt in self._appointments.values():
                if appt.doctor_id == doctor_id and appt.day == day and appt.start == start:
                    raise ValueError("slot already booked")

            appointment = Appointment(
                id=next(self._id_sequence),
                doctor_id=doctor_id,
                patient_id=patient_id,
                day=day,
                start=start,
                end=end,
            )
            self._appointments[appointment.id] = appointment
            return appointment

    def cancel_appointment(self, appointment_id: int) -> bool:
        with self._lock:
            return self._appointments.pop(appointment_id, None) is not None

    def _get_doctor(self, doctor_id: str) -> Doctor:
        doctor = self._doctors.get(doctor_id)
        if doctor is None:
            raise ValueError("doctor not found")
        return doctor

    def _validate_slot_bounds(self, doctor: Doctor, start: time) -> None:
        start_dt = datetime.combine(date.today(), start)
        open_dt = datetime.combine(date.today(), doctor.work_start)
        close_dt = datetime.combine(date.today(), doctor.work_end)

        if start_dt < open_dt:
            raise ValueError("slot outside working hours")

        if (start_dt - open_dt).total_seconds() % (SLOT_MINUTES * 60) != 0:
            raise ValueError("slot must start on a 30-minute boundary")

        if start_dt + timedelta(minutes=SLOT_MINUTES) > close_dt:
            raise ValueError("slot outside working hours")


def default_doctors() -> List[Doctor]:
    return [
        Doctor("doc-1", "Dr. Achieng", time(9, 0), time(17, 0)),
        Doctor("doc-2", "Dr. Kibet", time(9, 0), time(17, 0)),
        Doctor("doc-3", "Dr. Mwangi", time(9, 0), time(17, 0)),
        Doctor("doc-4", "Dr. Otieno", time(9, 0), time(17, 0)),
        Doctor("doc-5", "Dr. Wanjiru", time(9, 0), time(17, 0)),
    ]
