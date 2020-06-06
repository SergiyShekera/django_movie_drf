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


class MovieListView(APIView):
    """Вывод списка фильмов"""
    def get(self, request):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=Count(
                "ratings",
                filter=Q(
                    ratings__ip=get_client_ip(request)
                )
            )
        ).annotate(
            middle_star=(Avg("ratings__star"))
        )
        # ).annotate(
        #     middle_star=(Sum(F("ratings__star")) / Count(F("ratings")))
        # )
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    """Вывод фильма"""
    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    """Добавление отзыва к фильму"""
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddStarRatingView(APIView):
    """Добавление рейтинга фильму"""
    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)


class ActorsListView(generics.ListAPIView):
    """Вывод списка актеров"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorsDetailView(generics.RetrieveAPIView):
    """Вывод актера или режиссера"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
