from celery import shared_task
from .models import Contact
from django.conf import settings

from django_app.celery import app 
from .service import send
from django.core.mail import send_mail


@app.task
def send_spam(email):
    send(email)
@app.task
def send_mass_mail():
    for contact in Contact.objects.all():
        send_mail(
            'subject',
            'We will send you email every 10 mins',
            settings.EMAIL_HOST_USER,
            [contact.email],
            fail_silently=True
        )

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_widgets():
    return Widget.objects.count()

@app.task(bind=True, default_retry_delay=5*60)
def task_retry(self, x, y):
    try:
        return x + y
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)