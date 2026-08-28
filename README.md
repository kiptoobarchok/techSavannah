# techSavannah

techSavannah is a clinic booking platform for a small practice (starting with 5 doctors) and designed to scale.

## Technical Stack
- **API Layer:** Django (Django REST Framework)
- **Frontend Dashboards:** Next.js
- **Database:** PostgreSQL

## Core Scenario
Patients can:
- view available 30-minute slots per doctor per day,
- book a free slot,
- cancel an appointment,
- and ensure booked slots are no longer available to other patients.

---

## Roadmap & Blueprint (4 Sections)

The project will be delivered in four connected sections, where each section builds on the previous one.

### Section 1 — Product & System Design
**Goal:** Define exactly what we are building.

**Sprint 1.1: Domain Blueprint**
- Define users, roles, and flows (patient, doctor, admin).
- Define appointment rules (working hours, 30-minute slots, conflict rules, cancellation).
- Finalize core entities and relationships.

**Sprint 1.2: API & UX Blueprint**
- Draft API contracts for slot listing, booking, and cancellation.
- Draft dashboard wireframes (admin + doctor + patient views).
- Define acceptance criteria for Section 2 build.

### Section 2 — Application Build
**Goal:** Implement what was designed in Section 1.

**Sprint 2.1: Backend Foundation (Django + PostgreSQL)**
- Set up Django project, app modules, and PostgreSQL connection.
- Create models and migrations for doctors, patients, appointments, availability.
- Implement authentication/authorization baseline.

**Sprint 2.2: Booking Engine**
- Implement slot generation from doctor working hours.
- Implement free-slot retrieval by doctor/date.
- Implement booking with concurrency-safe conflict prevention.
- Implement cancellation and slot release logic.

**Sprint 2.3: Frontend Dashboards (Next.js)**
- Build patient booking flow UI.
- Build doctor schedule visibility.
- Build admin operational dashboard.

### Section 3 — Deployment & Operations
**Goal:** Deploy Section 2 deliverables and make them operational.

**Sprint 3.1: Release Preparation**
- Environment configuration (dev/staging/prod).
- Database migration/release process.
- Observability baseline (logs, error tracking, health checks).

**Sprint 3.2: Production Deployment**
- Deploy Django API and Next.js frontend.
- Configure PostgreSQL production instance.
- Validate end-to-end booking flows in production-like conditions.

### Section 4 — Scale, Quality, and Expansion
**Goal:** Improve reliability, performance, and feature depth.

**Sprint 4.1: Reliability & Performance**
- Add caching and query optimization.
- Strengthen transactional integrity and retry strategies.
- Expand automated test coverage.

**Sprint 4.2: Product Expansion**
- Add notifications/reminders.
- Add advanced scheduling rules and clinic reports.
- Prepare multi-clinic / larger-team scaling patterns.

---

## Feature Prioritization Blueprint (MoSCoW × RICE Hybrid)

We will prioritize work using two stages:

### Stage A — MoSCoW (Strategic Fit)
Classify each feature into:
- **Must Have:** required for core booking journey to function safely.
- **Should Have:** high-value improvements with moderate risk if delayed.
- **Could Have:** useful enhancements with low immediate impact.
- **Won’t Have (Now):** intentionally deferred to later sections.

### Stage B — RICE (Execution Order)
Inside each MoSCoW bucket, rank features with RICE:
- **Reach:** number of users/flows impacted.
- **Impact:** expected outcome improvement.
- **Confidence:** certainty of estimates and solution.
- **Effort:** implementation cost (lower effort increases priority).

**RICE Score Formula:**

`Priority Score = (Reach × Impact × Confidence) ÷ Effort`

### Prioritization Rule
1. Prioritize by MoSCoW bucket first (`Must > Should > Could > Won’t`).
2. Then sort by RICE score within each bucket.
3. Pull highest-ranked items into the next sprint.

---

## Initial Backlog Seed (Example)

### Must Have
- Doctor working-hour configuration
- 30-minute slot generation
- Free slot search by doctor/date
- Concurrency-safe appointment booking
- Appointment cancellation and slot release
- Basic authentication and role controls

### Should Have
- Doctor dashboard for daily schedule overview
- Admin dashboard for clinic utilization
- Audit logs for booking/cancellation actions

### Could Have
- Reminder notifications (email/SMS)
- Reschedule flow
- Search and filtering enhancements

### Won’t Have (Now)
- Multi-clinic tenancy
- AI-assisted schedule optimization

---

## Execution Principle
What is designed in **Section 1** is implemented in **Section 2** and deployed in **Section 3**. Section 4 extends quality, scale, and product depth.
