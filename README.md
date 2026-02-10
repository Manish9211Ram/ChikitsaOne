# ChikitsaOne - Medical Appointment System

A modern Python Web SaaS application built with **Django** and **SQLite3**, designed for efficient medical practice management.

## Features

- **Patient Registration**: New patients can register with their personal details.
- **Appointment Booking**: Patients can search by Adhaar number and book appointments with specialists.
- **Doctor Directory**: View a list of available doctors and their departments.
- **Services list**: Browse available medical services (X-Ray, MRI, etc.).
- **Doctor Dashboard**: secure login for doctors to view their scheduled appointments.
- **Admin Record View**: View all registered patient records.
- **Responsive Design**: Modern, glassmorphism-inspired UI with a dark theme.

## Prerequisites

- Python 3.8+
- Django 5.x/6.x
- Pandas (optional, if future analytics needed)

## Installation

1.  **Clone/Open the project folder**:
    ```bash
    cd c:\Users\manis\OneDrive\Desktop\ChikitsaOne
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Migrations** (Initial Setup):
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4.  **Poluate Initial Data** (Optional, auto-runs on first visit to Doctor list):
    ```bash
    python manage.py shell -c "from medical.views import populate_initial_data, populate_services; populate_initial_data(); populate_services()"
    ```

5.  **Run the Server**:
    ```bash
    python manage.py runserver
    ```

6.  **Access the App**:
    Open your browser and navigate to: `http://127.0.0.1:8000/`

## Usage Guide

- **Patients**: Click "Register Patient" to sign up. Then "Book Appt" to schedule a visit.
- **Doctors**: Login at `/doctor/login/`. Use your Doctor ID as both ID and Password (e.g., `7001`).
    - *Common Doctor IDs*:
        - Dr. Varun: 7001
        - Dr. Hrithik: 7002
        - Dr. Salman: 7003

## Technology Stack

- **Backend**: Django (Python)
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3 (Custom Glassmorphism Theme) 

---
*Created by Antigravity*
