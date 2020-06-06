from django.db.models import Avg, Count, Sum, Q, F

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie, Actor
from .serializers import (
    ActorDetailSerializer,
    ActorListSerializer,
    CreateRatingSerializer,
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
)

from .service import get_client_ip


class MovieListView(generics.ListAPIView):
    """Вывод списка фильмов"""

    serializer_class = MovieListSerializer

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=Count(
                "ratings",
                filter=Q(
                    ratings__ip=get_client_ip(self.request)
                )
            )
        ).annotate(
            middle_star=(Avg("ratings__star"))
        )
        # ).annotate(
        #     middle_star=(Sum(F("ratings__star")) / Count(F("ratings")))
        # )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """Вывод фильма"""
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateView(generics.CreateAPIView):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer


class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsListView(generics.ListAPIView):
    """Вывод списка актеров"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorsDetailView(generics.RetrieveAPIView):
    """Вывод актера или режиссера"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
