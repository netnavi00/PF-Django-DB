from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import TBL_Usuario, TBL_Video, TBL_Usuario_Video

# Formatos de video permitidos
EXTENSIONES_PERMITIDAS = ['mp4', 'avi', 'mov', 'mkv', 'webm']
MAX_TAMANO_MB = 3
MAX_BYTES = MAX_TAMANO_MB * 1024 * 1024  # 3,145,728 bytes

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
        nombre_usuario = request.POST.get('nombre_usuario', '')
        cantidad = int(request.POST.get('cantidad', 0))

        # 1. Validar que no falten datos ni archivos
        for i in range(1, cantidad + 1):
            archivo_obj = request.FILES.get(f'archivo_{i}')
            nombre_vid = request.POST.get(f'nombre_video_{i}', '').strip()

            # A) Validar si falta el archivo
            if not archivo_obj:
                return render(request, 'streaming/paso2.html', {
                    'id_nomina': id_nomina,
                    'nombre_usuario': nombre_usuario,
                    'cantidad': cantidad,
                    'rango_videos': range(1, cantidad + 1),
                    'error': f'Revisar formulario: Falta adjuntar el archivo de video para el elemento #{i}.'
                })

            # B) Validar si falta el nombre/título del video
            if not nombre_vid:
                return render(request, 'streaming/paso2.html', {
                    'id_nomina': id_nomina,
                    'nombre_usuario': nombre_usuario,
                    'cantidad': cantidad,
                    'rango_videos': range(1, cantidad + 1),
                    'error': f'Revisar formulario: El título o nombre para el video #{i} no puede estar vacío.'
                })

            # C) Validar Extensión
            ext = archivo_obj.name.split('.')[-1].lower()
            if ext not in EXTENSIONES_PERMITIDAS:
                return render(request, 'streaming/paso2.html', {
                    'id_nomina': id_nomina,
                    'nombre_usuario': nombre_usuario,
                    'cantidad': cantidad,
                    'rango_videos': range(1, cantidad + 1),
                    'error': f'Revisar archivo: "{archivo_obj.name}" no es un video permitido. Solo se aceptan extensiones: {", ".join(EXTENSIONES_PERMITIDAS)}.'
                })

            # D) Validar Tamaño (Máximo 3 MB)
            if archivo_obj.size > MAX_BYTES:
                tamano_actual_mb = round(archivo_obj.size / (1024 * 1024), 2)
                return render(request, 'streaming/paso2.html', {
                    'id_nomina': id_nomina,
                    'nombre_usuario': nombre_usuario,
                    'cantidad': cantidad,
                    'rango_videos': range(1, cantidad + 1),
                    'error': f'Revisar archivo: "{archivo_obj.name}" pesa {tamano_actual_mb} MB. El límite máximo permitido es de {MAX_TAMANO_MB} MB.'
                })        

        # 2. Buscar usuario
        try:
            usuario = TBL_Usuario.objects.get(id_nomina=id_nomina)
            print(f"Usuario encontrado: {usuario.nombre}")
        except TBL_Usuario.DoesNotExist:
            print("❌ ERROR: El usuario no existe con esa nómina.")
            usuario = None

        # 3. Guardar en BD
        for i in range(1, cantidad + 1):
            archivo_obj = request.FILES.get(f'archivo_{i}')
            nombre_vid = request.POST.get(f'nombre_video_{i}')

            print(f"Video {i}: archivo={archivo_obj}, nombre={nombre_vid}")

            if archivo_obj:
                ext = archivo_obj.name.split('.')[-1].lower()[:5]

                # Instanciar el objeto
                video = TBL_Video(
                    nombre=nombre_vid if nombre_vid else archivo_obj.name,
                    extension=ext,
                    tamano=int(archivo_obj.size / (1024 * 1024)),  # MB
                    archivo=archivo_obj
                )
                
                # Dispara las validaciones internas de Django
                try:
                    video.full_clean()
                    video.save()
                    print(f"✅ Video creado en BD con ID: {video.id_video}")

                    if usuario:
                        TBL_Usuario_Video.objects.create(id_usuario=usuario, id_video=video)
                        print("✅ Relación TBL_Usuario_Video creada correctamente")
                except ValidationError as e:
                    print(f"❌ Error de validación en video {i}: {e}")

        return render(request, 'streaming/exito.html', {'mensaje': '¡Videos guardados con éxito!'})

    return redirect('paso1')