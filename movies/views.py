from django.db.models import Avg, Count, Sum, Q, F

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, permissions, viewsets
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

from .service import get_client_ip, MovieFilter


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод списка фильмов"""
    filter_backends = (DjangoFilterBackend, )
    filterset_class = MovieFilter

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
        return movies

    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer
        elif self.action == "retrieve":
            return MovieDetailSerializer


# class MovieListView(generics.ListAPIView):
#     """Вывод списка фильмов"""
#     serializer_class = MovieListSerializer
#     filter_backends = (DjangoFilterBackend, )
#     filterset_class = MovieFilter
#
#     # permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=Count(
#                 "ratings",
#                 filter=Q(
#                     ratings__ip=get_client_ip(self.request)
#                 )
#             )
#         ).annotate(
#             middle_star=(Avg("ratings__star"))
#         )
#         # ).annotate(
#         #     middle_star=(Sum(F("ratings__star")) / Count(F("ratings")))
#         # )
#         return movies


class MovieDetailView(generics.RetrieveAPIView):
    """Вывод фильма"""
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer


# class ReviewCreateView(generics.CreateAPIView):
#     """Добавление отзыва к фильму"""
#     serializer_class = ReviewCreateSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
    """Добавление рейтинга фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


# class AddStarRatingView(generics.CreateAPIView):
#     """Добавление рейтинга фильму"""
#     serializer_class = CreateRatingSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(ip=get_client_ip(self.request))


class ActorsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод актеров или режиссеров"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ActorListSerializer
        elif self.action == "retrieve":
            return ActorDetailSerializer


# class ActorsListView(generics.ListAPIView):
#     """Вывод списка актеров"""
#     queryset = Actor.objects.all()
#     serializer_class = ActorListSerializer
#
#
# class ActorsDetailView(generics.RetrieveAPIView):
#     """Вывод актера или режиссера"""
#     queryset = Actor.objects.all()
#     serializer_class = ActorDetailSerializer
