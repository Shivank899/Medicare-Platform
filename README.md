# Online Doctor Appointment System

Medicare+ is a premium, full-stack healthcare platform built with Python Flask and MySQL.

## Features
- **Three-tier Architecture:** Clean separation of models, routes, and views.
- **Role-based Auth:** Specific dashboards for Patients, Doctors, and Admins.
- **Modern UI:** Premium design with Inter typography, glassmorphism, and dark mode.
- **Security:** Password hashing (bcrypt), CSRF protection, and SQL injection prevention.
- **Responsive:** Works perfectly on Mobile, Tablet, and Desktop.

## Tech Stack
- **Frontend:** HTML5, CSS3 (Modular), Vanilla JS
- **Backend:** Python Flask
- **Database:** MySQL (Supports SQLite fallback)
- **ORM:** SQLAlchemy

## Installation

1. **Clone/Download the project**
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Database:**
   Edit `.env` or `config/config.py` with your MySQL credentials.
   Default: Uses `site.db` (SQLite) for immediate run.
4. **Seed Database:**
   ```bash
   flask seed-db
   ```
5. **Run the Application:**
   ```bash
   python app.py
   ```

## Default Credentials
- **Admin:** admin@medicare.com / admin123
- **Doctor:** sarah@medicare.com / doctor123
- **Patient:** (Register via UI)

## Security Features
- Bcrypt hashing for all passwords.
- Role-based route protection.
- Input validation and sanitization via WTForms.
- CSRF protection enabled on all forms.
