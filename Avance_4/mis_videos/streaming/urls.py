from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.paso1_view, name='paso1'),
    path('procesar-usuario/', views.procesar_paso1, name='procesar_paso1'),
    path('guardar-videos/', views.guardar_videos, name='guardar_videos'),
    path('videos/', views.lista_videos, name='lista_videos'),  # Ruta para ver los videos
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)