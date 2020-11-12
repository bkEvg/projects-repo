from rest_framework import generics
from django.db import models 

from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Review, Actor
from .serializers import (MovieListSerializer, 
                        MovieDetailSerializer, 
                        ReviewCreateSerializer,
                        CreateRatingSerializer,
                        ActorListSerializer,
                        ActorDetailSerializer)

from .service import get_client_ip, MovieFilter


class MovieListView(generics.ListAPIView):
    """Вывод списка фильмов"""
    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        """Returns queryset"""
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star__value')) / models.Count(models.F('ratings'))
        )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """Movie Detail View"""

    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateView(generics.CreateAPIView):
    """Review Create View"""
    serializer_class = ReviewCreateSerializer

    
class AddRatingStarView(generics.CreateAPIView):
    """Adding rating to movie"""
    serializer_class = CreateRatingSerializer
    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsListView(generics.ListAPIView):
    """Actor list view"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer