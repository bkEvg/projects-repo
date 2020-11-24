from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView
from .models import Contact
from .forms import ContactForm
from .service import send
from .tasks import send_spam

# def contact(request):
#     form = ContactForm()
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
            
#             Contact.objects.create(name=cd['name'], email=cd['email'])
#             send_spam.delay(form.instance.email) #delay says let's not wait
#             return HttpResponse('ok')
#     return render(request, 'myapp/contact.html', {'form': form})

class ContactView(CreateView):
    model = Contact
    success_url = '/send'
    form_class = ContactForm

    def form_valid(self, form):
        form.save()
        send_spam.delay(form.instance.email) #delay says let's not wait
        return super().form_valid(form)
