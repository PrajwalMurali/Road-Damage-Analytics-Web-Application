# Road Damage Analytics Web Application

A Django-based web application for reporting and tracking road damage complaints submitted by citizens. The platform allows users to register, log in, submit complaints with supporting images, and monitor their status. Admin users can review complaints, manage user approvals, and oversee analytics for maintenance planning.

## Features

- Citizen complaint submission
- Road damage reporting with location and severity
- Photo upload as evidence
- User registration and approval workflow
- Admin dashboard with complaint analytics
- Complaint listing, editing, and deletion
- Django ORM-based CRUD operations
- SQLite database for local project use

## Tech Stack

- Python
- Django
- SQLite
- HTML
- CSS

## Project Structure

- `lab3project/` - Django project configuration
- `main/` - application logic, models, views, URLs
- `templates/` - HTML templates for pages
- `static/` - CSS files
- `media/` - uploaded complaint images
- `db.sqlite3` - SQLite database file

## Setup Instructions

1. Clone the repository
   ```bash
   git clone https://github.com/PrajwalMurali/Road-Damage-Analytics-Web-Application.git
   cd Road-Damage-Analytics-Web-Application
   ```

2. Create and activate a virtual environment (optional but recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install django pillow
   ```

4. Run database migrations and create the default users
   ```bash
   python manage.py migrate
   python manage.py create_default_users
   ```

5. Start the development server
   ```bash
   python manage.py runserver
   ```

6. Open the app in a browser
   ```text
   http://127.0.0.1:8000/
   ```

## Default Login Credentials

### Admin
- Username: `admin`
- Password: `admin123`

### Citizen
- Username: `citizen`
- Password: `citizen123`

These accounts are created automatically when you run `python manage.py create_default_users`.

## User Workflow

1. Register a new account.
2. Wait for admin approval.
3. Log in once approved.
4. Submit a road damage complaint with proof photo.
5. Admin can review and manage complaints from the dashboard.

## Notes

This project is intended for academic learning and demonstration of Django CRUD operations, authentication flow, and a civic complaint management use case.

## License

This project is for educational purposes.
