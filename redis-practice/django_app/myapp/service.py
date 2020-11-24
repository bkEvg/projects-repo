from django.core.mail import send_mail
from django.conf import settings

def send(email):
    return send_mail(
        'Subject here',
        'Here is the message.',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=True,
    )





