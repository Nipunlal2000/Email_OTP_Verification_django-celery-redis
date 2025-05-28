from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from datetime import datetime
from django.utils.dateparse import parse_datetime

@shared_task
def send_otp_email(email, otp):
    
    print(f"[CELERY TASK] 🔛 Sending OTP to {email}: {otp}")
    
    subject = "Email Verification OTP"
    message = f"Your OTP is: {otp}"
    from_email = settings.EMAIL_HOST_USER
    recipient = ['siddarthnair88@gmail.com']
    
    send_mail(subject, message, from_email, recipient)


# @shared_task
# def send_hourly_user_report():
#     total_users = UserProfile.objects.count()
#     verified_users = UserProfile.objects.filter(is_email_verified=True).count()
#     unverified_users = total_users - verified_users

#     subject = "⏱️ Hourly User Report"
#     message = (
#         f"Total Users: {total_users}\n"
#         f"Verified Users: {verified_users}\n"
#         f"Unverified Users: {unverified_users}\n"
#     )
#     recipient = ['admin@gmail.com']  # Change to your admin email
#     from_email = settings.EMAIL_HOST_USER

#     send_mail(subject, message, from_email, recipient, fail_silently=False,)
    # print("📤 Hourly user report sent to admin.")
    

@shared_task
def schedule_appointment_reminder(email, title, time):

    # Parse string datetime with timezone support
    if isinstance(time, str):
        time = parse_datetime(time)

    formatted_time = time.strftime("at %d-%m-%Y on %I:%M %p")


    # Extract name from email
    name = email.split('@')[0].capitalize()
    
    subject = f"📅 Reminder: Your '{title}' appointment is coming up!"
    message = (
        f"Hi {name}✋,\n\n"
        f"This is a gentle reminder from Neurocode.\n"
        f"You have an appointment titled '{title}' scheduled {formatted_time}.\n\n"
        f"Best regards,\nTeam Neurocode"
    )
    from_email = settings.EMAIL_HOST_USER
    recipient = ['siddarthnair88@gmail.com']  # Change to your admin email
    fail_silently = False
    
    send_mail(subject, message, from_email, recipient, fail_silently)
    print(f"📤 Reminder email sent to {email}")
    
