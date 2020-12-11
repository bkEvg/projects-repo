from django.shortcuts import render
from django.views.generic import CreateView
from .forms import ContactForm 
from .models import Contact
from .tasks import send_mail



class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        send_mail.delay(form.instance.email)
        return super().form_valid(form)