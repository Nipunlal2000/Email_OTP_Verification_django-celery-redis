# 📧 Email Confirmation System with DRF, Celery & Redis

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.0-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14+-red.svg)](https://www.django-rest-framework.org/)
[![Celery](https://img.shields.io/badge/Celery-5.3+-brightgreen)](https://docs.celeryq.dev/)
[![Redis](https://img.shields.io/badge/Redis-7+-red)](https://redis.io/)
[![Postgres](https://img.shields.io/badge/DB-PostgreSQL-blue)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

This is a secure **Email Confirmation System** built using Django REST Framework. It includes:

- User registration and login using JWT.
- OTP email verification with expiration (3 mins).
- Redis for in-memory OTP caching.
- Celery for asynchronous OTP email delivery.

---

## 🔧 Tech Stack

- **Backend:** Django, Django REST Framework  
- **Authentication:** JWT (SimpleJWT)  
- **Async Task Queue:** Celery  
- **Caching:** Redis  
- **Broker:** Redis  
- **Database:** PostgreSQL (can use SQLite during development)

---

## 🚀 Features

- ✅ Register with email and password  
- ✅ Email verification via OTP  
- ✅ OTP cached in Redis for 3 minutes  
- ✅ Celery sends OTP asynchronously  
- ✅ Retry OTP feature  
- ✅ JWT-based login and authentication

---

## 🗂️ Project Structure

email_confirmation_sys/ <br>
├── email_confirmation_sys/ <br>
│ └── settings.py <br>
├── email_app/ <br>
│ ├── models.py <br>
│ ├── views.py <br>
│ ├── serializers.py <br>
│ ├── tasks.py <br>
│ ├── signals.py <br>
│ └── urls.py <br>
├── manage.py <br>
└── requirements.txt

---

## ⚙️ Setup Instructions

### 1. Clone the repository

git clone https://github.com/Nipunlal2000/email-confirmation-sys.git <br>
cd email-confirmation-sys

### 2. Create a virtual environment and install requirements

python -m venv venv <br>
source venv/bin/activate  <br>
(For Windows: venv\Scripts\activate) <br>
pip install -r requirements.txt

### 3. Update `.env` or `settings.py` for:

- Redis URL  
- Email credentials

### 4. Apply migrations and run the server

python manage.py makemigrations <br>
python manage.py migrate <br>
python manage.py runserver

### 5. Start Redis Server

redis-server

### 6. Start Celery Worker

celery -A email_confirmation_sys worker --loglevel=info --pool=solo

### 7. Register and verify email

- Register: POST `/api/register/` <br>
- Send OTP: POST `/api/send-otp/` <br>
- Verify OTP: POST `/api/verify-otp/` <br>
- Login: POST `/api/login/`

---

## 📬 Environment Variables (Sample)

EMAIL_HOST=smtp.gmail.com <br>
EMAIL_PORT=587 <br>
EMAIL_USE_TLS=True <br>
EMAIL_HOST_USER=your_email@gmail.com <br>
EMAIL_HOST_PASSWORD=your_password <br>
REDIS_URL=redis://localhost:6379/0 <br>

---

## 🔁 Redis & OTP Notes

- OTP is cached in Redis and expires after 3 minutes.  
- You can resend OTP if the time expires via the resend endpoint.

---

## 🧪 Testing

- Use Postman or cURL to test endpoints.  
- Celery logs and Redis data can be monitored during testing.

---

## 📅 Scheduled Email Notifications for Appointments

A new feature is integrated for scheduling appointment reminders:

- Admin receives an email notification when a user creates an appointment.  
- The email includes the user’s name (parsed from their email) and the scheduled time in a friendly format:  
  **"at DD-MM-YYYY on HH:MM AM/PM"**.  
- Implemented using:
  - `Appointment` model  
  - `AppointmentSerializer`  
  - `AppointmentCreateView` (APIView)  
  - Django `signals.py` (emits event on creation)  
  - Celery `tasks.py` (handles formatted email dispatch)

### Example Email Message

```
Hi Nipun 👋, <br>
This is from Neurocode 🧠. <br>
You have an appointment scheduled at 28-05-2025 on 10:30 AM. <br>
See you soon!
```
---

## 💡 Author

Developed by Nipun Lal Rc
