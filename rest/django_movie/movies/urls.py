from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = format_suffix_patterns([
    path("movie/", views.MovieViewSet.as_view({'get': 'list'})),
    path("movie/<int:pk>/", views.MovieViewSet.as_view({'get': 'retrieve'})),
    path("review/", views.ReviewCreateViewSet.as_view({'post': 'create'})),
    path("rating/", views.AddRatingViewSet.as_view({'post': 'create'})),
    path('actor/', views.ReviewCreateViewSet.as_view({'get': 'list'})),
    path('actor/<int:pk>/', views.ReviewCreateViewSet.as_view({'get': 'retrieve'})),
])