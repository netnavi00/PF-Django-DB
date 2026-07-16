from django.urls import path
from . import views

urlpatterns = [
    path('', views.paso1_view, name='paso1'),
    path('procesar-usuario/', views.procesar_paso1, name='procesar_paso1'),
    path('guardar-videos/', views.guardar_videos, name='guardar_videos'),
]