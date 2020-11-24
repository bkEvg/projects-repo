from django.urls import path
from . import views


urlpatterns = [
    path('send/', views.ContactView.as_view(), name='send')
]
