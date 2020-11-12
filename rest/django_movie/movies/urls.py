from django.urls import path
from . import views


urlpatterns = [
    path('movies/', views.MovieListView.as_view()),
    path('movies/<int:pk>/', views.MovieDetailView.as_view()),
    path('reviews/', views.ReviewCreateView.as_view()),
    path('rating/', views.AddRatingStarView.as_view()),
    path('actors/', views.ActorsListView.as_view()),
    path('actors/<int:pk>/', views.ActorDetailView.as_view()),
]