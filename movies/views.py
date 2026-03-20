from django.db.models import Count, Avg
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermission
from movies.models import Movie
from movies.serializers import MovieSerializer, MovieStatsSerializer
from reviews.models import Review


class MovieListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieStatsAPIView(APIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Movie.objects.all()

    def get(self, request):
        total_movies = self.queryset.count()
        movies_by_genre = self.queryset.values('genre__name').annotate(
            count=Count('id')
        ).order_by('-count')
        total_reviews = Review.objects.count()
        average_rating = Review.objects.aggregate(average=Avg('stars'))['average']

        data = {
            'total_movies': total_movies,
            'movies_by_genre': movies_by_genre,
            'total_reviews': total_reviews,
            'average_rating': round(average_rating, 1) if average_rating else 0,
        }

        serializer = MovieStatsSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.validated_data,
            status=HTTP_200_OK
        )
