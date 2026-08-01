# techSavannah

This project provides a small clinic appointment API for 5 doctors.

## Features
- Doctors have fixed working hours (09:00-17:00)
- 30-minute appointment slots
- Patients can view free slots for a doctor on a specific date
- Booking removes the slot from availability
- Cancellation releases the slot back to availability

## Run
```bash
cd /home/runner/work/techSavannah/techSavannah
PYTHONPATH=src python -m clinic_booking.api
```

## API
- `GET /doctors`
- `GET /doctors/{doctor_id}/slots?date=YYYY-MM-DD`
- `POST /appointments`
  - Body: `{"doctor_id":"doc-1","date":"2026-08-01","start_time":"10:00","patient_id":"patient-1"}`
- `DELETE /appointments/{appointment_id}`

## Test
```bash
cd /home/runner/work/techSavannah/techSavannah
PYTHONPATH=src python -m unittest tests/test_service.py -v
```
