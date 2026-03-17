from django.urls import path
from . import views


urlpatterns = [
    path('actors/', views.ActorListCreateAPIView.as_view(), name='actor-create-list'),
    path('actors/<int:pk>/', views.ActorRetrieveUpdateDestroyAPIView.as_view(), name='actor-detail'),
]
