from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView
from .models import Contact
from .forms import ContactForm
from .service import send

def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            
            Contact.objects.create(name=cd['name'], email=cd['email'])
            send(form.instance.email)
            return HttpResponse('ok')
    return render(request, 'myapp/contact.html', {'form': form})
