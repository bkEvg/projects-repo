from proj.celery import app
from .helpers import send
from django.core.mail import send_mail
from .models import Contact
from django.conf import settings


@app.task
def send_mail(email):
    send(email)


@app.task
def send_mail_every_month():
    for contact in Contact.objects.all():
        send_mail(
            'Hellp',
            'We have not seen you for a long time!',
            settings.EMAIL_USER,
            [contact.email],
            fail_silently=True
        )
