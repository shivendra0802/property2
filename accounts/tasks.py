from __future__ import absolute_import, unicode_literals
from celery import shared_task

@shared_task(bind=True)
def test_func(self):
    #operations
    for i in range(10):
        print(i)
    return "Done"


from django.contrib.auth import get_user_model

# from celery import shared_task
from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from btre import settings
from datetime import timedelta

@shared_task(bind=True)
def send_mail_func(self):
    users = get_user_model().objects.all()
    # timezone.localtime(users.date_time)
    for user in users:
        mail_subject = "Hi! Celery Testing"
        message = "Thanku for signup"
        to_email = user.email
        send_mail(
            subject = mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
    return "Done"