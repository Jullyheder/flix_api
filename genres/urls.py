from django.urls import path
from . import views


urlpatterns = [
    path('genres/', views.GenreListCreateAPIView.as_view(), name='genre-create-list'),
    path('genres/<int:pk>/', views.GenreRetrieveUpdateDestroyAPIView.as_view(), name='genre-detail'),
]
