# TechSavannah

TechSavannah is a clinic booking platform built for a small medical practice with five doctors and growing patient demand. The core goal is to let patients discover available 30-minute appointment slots for a doctor, book one safely, and cancel when needed without double-booking.

The backend is implemented with Django and Django REST Framework, with PostgreSQL as the database. The current codebase already models doctors, patients, and appointments, and the next stages focus on user management, authentication, slot availability, and cancellation workflows.

## Product Scope

### Primary users

- Doctors: view their schedule, appointments, availability, and clinic context.
- Patients: search availability, book appointments, and cancel their own bookings.
- Administrators: manage doctors, patients, and appointments through Django admin and/or a future custom admin UI.

### MVP business rules

- Appointments are always 30 minutes long.
- Each doctor has working hours and only those hours should produce bookable slots.
- Available slots are generated dynamically at request time instead of being pre-created in the database.
- Once a slot is booked, it is unavailable to other patients.
- Patients can cancel their own bookings.
- The system should be safe under concurrent booking attempts.

### User management strategy

This project starts with a simple, pragmatic identity model:

- Doctors have access to authenticated tools for schedules, appointments, and availability management.
- Patients can book without a full account in the earliest MVP stage.
- A patient record may be created or fetched automatically during booking using a unique email address.
- Appointment UUIDs can be used as secure cancelation tokens so patients can cancel their own bookings without needing a full login flow.
- Doctor/admin access can initially be handled through Django admin, with a custom Next.js admin experience added later.

## System Design

### Core domain model

- Doctor: clinic staff member with identity, specialty, and active status.
- Patient: booking identity with contact details.
- Appointment: a reserved 30-minute slot that links one doctor and one patient.

### Booking flow

1. A patient selects a doctor and a day.
2. The backend generates all valid 30-minute slots inside that doctor’s working hours.
3. The API subtracts existing appointments to determine free slots.
4. The patient submits a desired slot.
5. The booking service validates the time window and reserves it inside a database transaction.
6. If another request already claimed the same slot, the API rejects the request.

### Concurrency approach

- Slot uniqueness is enforced at the database level.
- Booking runs inside an atomic transaction.
- The application relies on database constraints and transactional checks to prevent two patients from getting the same slot.
- This design keeps the slot source of truth in the appointments table rather than in a separate inventory table.

### Cancellation flow

- A patient cancels an appointment using a UUID-based reference.
- The appointment is marked cancelled or removed depending on the final policy.
- Once cancelled, the slot becomes available again for future booking.

## Implementation Stages

### Stage 1: Core booking engine

- Dynamic slot generation.
- Appointment creation and validation.
- Transaction-safe concurrency handling.
- Cancelation support.

### Stage 2: User management

- Doctor authentication and access control.
- Patient auto-creation or lookup by email.
- Appointment UUID-based patient cancelation.

### Stage 3: Doctor experience

- Doctor dashboards for personal schedules.
- Availability views for colleagues and shared clinic context.
- Admin tools for operational management.

### Stage 4: Product growth

- Rescheduling.
- Expanded patient metadata.
- CI/CD and cloud deployment.

## Current Backend Structure

- `booking.models` defines `Doctor`, `Patient`, and `Appointment`.
- `booking.services` contains appointment booking validation and transaction logic.
- `booking.repositories` centralizes database access patterns.
- `booking.serializers` exposes the REST API contract.
- `booking.views` provides list/create endpoints for doctors, patients, and appointments.

## Current API Surface

- `GET /doctors/` and `POST /doctors/`
- `GET /patients/` and `POST /patients/`
- `GET /appointments/` and `POST /appointments/`

## Technical Notes

- PostgreSQL is used for persistence.
- Django time zone handling is enabled.
- REST Framework is configured for JSON-first APIs.
- CORS is enabled for the Next.js frontend.

## Next Step

The next implementation milestone is to add secure patient booking/cancellation flows and availability endpoints that expose free 30-minute slots per doctor per day.
