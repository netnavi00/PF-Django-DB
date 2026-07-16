from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import TBL_Usuario, TBL_Video, TBL_Usuario_Video

# Renderiza la primera pantalla (Datos de Usuario)
def paso1_view(request):
    return render(request, 'streaming/paso1.html')

# Procesa el primer formulario y redirige a la captura de videos
def procesar_paso1(request):
    if request.method == 'POST':
        id_nomina = request.POST.get('id_nomina').strip()
        nombre = request.POST.get('nombre').strip()
        cantidad = int(request.POST.get('cantidad').strip())

        # Creamos un rango numérico para iterar sobre los N videos en el HTML
        rango_videos = range(1, cantidad + 1)

        context = {
            'id_nomina': id_nomina,
            'nombre_usuario': nombre,
            'cantidad': cantidad,
            'rango_videos': rango_videos
        }
        return render(request, 'streaming/paso2.html', context)
    return redirect('paso1')

# Recibe los N videos, los valida y los guarda en la Base de Datos PostgreSQL
def guardar_videos(request):
    if request.method == 'POST':
        id_nomina = request.POST.get('id_nomina')
        nombre_usuario = request.POST.get('nombre_usuario')
        cantidad = int(request.POST.get('cantidad'))

        try:
            # 1. Guardar o actualizar el usuario en la BD
            usuario_db, created = TBL_Usuario.objects.update_or_create(
                id_nomina=id_nomina,
                defaults={'nombre': nombre_usuario}
            )

            # 2. Ciclo iterativo para extraer y guardar cada uno de los N videos
            for i in range(1, cantidad + 1):
                titulo = request.POST.get(f'titulo_{i}').strip()
                nombre_video = request.POST.get(f'nombre_video_{i}').strip()
                extension = request.POST.get(f'extension_{i}').strip()
                tamano = int(float(request.POST.get(f'tamano_{i}').strip()))

                # Guardamos el video en la tabla TBL_Video
                video_db = TBL_Video.objects.create(
                    nombre=nombre_video,
                    extension=extension if extension.startswith('.') else f".{extension}",
                    tamano=tamano
                )

                # Creamos el registro en la tabla de relación intermedia
                TBL_Usuario_Video.objects.create(
                    id_usuario=usuario_db,
                    id_video=video_db
                )

            return HttpResponse("<h2>[ÉXITO] Toda la información ha sido almacenada correctamente en PostgreSQL.</h2><br><a href='/'>Volver al inicio</a>")

        except Exception as e:
            return HttpResponse(f"<h2>[ERROR] Ocurrió un problema al guardar en la base de datos: {e}</h2>")

    return redirect('paso1')