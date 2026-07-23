from urllib import request

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
        print("--- INICIANDO GUARDADO DE VIDEOS ---")
        print("POST recibi-do:", request.POST)
        print("FILES recibi-dos:", request.FILES)  # <- Si esto está vacío {}, falta enctype en el HTML

        id_nomina = request.POST.get('id_nomina')
        cantidad = int(request.POST.get('cantidad', 0))

        try:
            usuario = TBL_Usuario.objects.get(id_nomina=id_nomina)
            print(f"Usuario encontrado: {usuario.nombre}")
        except TBL_Usuario.DoesNotExist:
            print("❌ ERROR: El usuario no existe con esa nómina.")
            usuario = None

        for i in range(1, cantidad + 1):
            archivo_obj = request.FILES.get(f'archivo_{i}')
            nombre_vid = request.POST.get(f'nombre_video_{i}')

            print(f"Video {i}: archivo={archivo_obj}, nombre={nombre_vid}")

            if archivo_obj:
                ext = archivo_obj.name.split('.')[-1].lower()[:5]
                
                # Crear registro
                video = TBL_Video.objects.create(
                    nombre=nombre_vid if nombre_vid else archivo_obj.name,
                    extension=ext,
                    tamano=int(archivo_obj.size / (1024 * 1024)), # MB
                    archivo=archivo_obj
                )
                print(f"✅ Video creado en BD con ID: {video.id_video}")

                if usuario:
                    TBL_Usuario_Video.objects.create(id_usuario=usuario, id_video=video)
                    print("✅ Relación TBL_Usuario_Video creada correctamente")

        return render(request, 'streaming/exito.html', {'mensaje': '¡Videos guardados con éxito!'})

    return redirect('paso1')