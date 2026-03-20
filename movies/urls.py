from django.urls import path
from . import views


urlpatterns = [
    path('movies/', views.MovieListCreateAPIView.as_view(), name='movie-list-create'),
    path('movies/<int:pk>/', views.MovieRetrieveUpdateDestroyAPIView.as_view(), name='movie-detail'),
    path('movies/stats/', views.MovieStatsAPIView.as_view(), name='movie-stats'),
]
