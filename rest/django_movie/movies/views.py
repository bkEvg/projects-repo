from rest_framework import generics, permissions, viewsets
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


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Display list of movies"""
    filter_backends = DjangoFilterBackend
    filterset_class = MovieFilter

    def get_queryset(self):
        """Returns queryset"""
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star__value')) / models.Count(models.F('ratings'))
        )
        return movies


class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    """Return actors and directors"""
    queryset = Actor.objects.all()
    def get_queryset(self):
        if self.action == 'get':
            return ActorListSerializer
        elif self.action == 'retreive':
            return ActorDetailSerializer

class ReviewCreateViewSet(viewsets.ModelViewSet):
    """Create review"""
    serializer_class = ReviewCreateSerializer


class AddRatingViewSet(viewsets.ModelViewSet):
    """Create rating"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))




# class MovieListView(generics.ListAPIView):
#     """Вывод списка фильмов"""
#     serializer_class = MovieListSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = MovieFilter

#     def get_queryset(self):
#         """Returns queryset"""
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
#         ).annotate(
#             middle_star=models.Sum(models.F('ratings__star__value')) / models.Count(models.F('ratings'))
#         )
#         return movies


# class MovieDetailView(generics.RetrieveAPIView):
#     """Movie Detail View"""

#     queryset = Movie.objects.filter(draft=False)
#     serializer_class = MovieDetailSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class ReviewCreateView(generics.CreateAPIView):
#     """Review Create View"""
#     serializer_class = ReviewCreateSerializer


# class ReviewDestroy(generics.DestroyAPIView):
#     """Deleting reviews"""
    
    
# class AddRatingStarView(generics.CreateAPIView):
#     """Adding rating to movie"""
#     serializer_class = CreateRatingSerializer
#     def perform_create(self, serializer):
#         serializer.save(ip=get_client_ip(self.request))


# class ActorsListView(generics.ListAPIView):
#     """Actor list view"""
#     queryset = Actor.objects.all()
#     serializer_class = ActorListSerializer


# class ActorDetailView(generics.RetrieveAPIView):
#     queryset = Actor.objects.all()
#     serializer_class = ActorDetailSerializer