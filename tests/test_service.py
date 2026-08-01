from datetime import date, time
import unittest

from clinic_booking.service import AppointmentService, default_doctors


class AppointmentServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = AppointmentService(default_doctors())
        self.day = date(2026, 8, 1)

    def test_lists_free_slots_in_30_minute_intervals(self):
        slots = self.service.list_free_slots("doc-1", self.day)
        self.assertEqual(time(9, 0), slots[0])
        self.assertEqual(time(16, 30), slots[-1])
        self.assertEqual(16, len(slots))

    def test_slot_becomes_unavailable_after_booking(self):
        self.service.book_slot("doc-1", self.day, time(10, 0), "patient-1")
        slots = self.service.list_free_slots("doc-1", self.day)
        self.assertNotIn(time(10, 0), slots)

    def test_cannot_double_book_same_doctor_slot(self):
        self.service.book_slot("doc-1", self.day, time(11, 0), "patient-1")
        with self.assertRaisesRegex(ValueError, "slot already booked"):
            self.service.book_slot("doc-1", self.day, time(11, 0), "patient-2")

    def test_cancel_makes_slot_available_again(self):
        appt = self.service.book_slot("doc-1", self.day, time(14, 30), "patient-1")
        self.service.cancel_appointment(appt.id)
        slots = self.service.list_free_slots("doc-1", self.day)
        self.assertIn(time(14, 30), slots)


if __name__ == "__main__":
    unittest.main()
