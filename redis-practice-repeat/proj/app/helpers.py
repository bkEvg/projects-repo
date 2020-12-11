from django.core.mail import send_mail
from django.conf import settings

def send(email):
    send_mail(
        'Here is a title',
        'Here is a body',
        settings.EMAIL_USER,
        [email],
        fail_silently=True
    )
