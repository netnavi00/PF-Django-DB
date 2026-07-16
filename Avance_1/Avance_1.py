import re
import sys

# =====================================================================
# FUNCIÓN ÚNICA PARA MOSTRAR MENSAJES DE ERROR
# =====================================================================
def mostrar_error(tipo_error):
    """
    Despliega los letreros de validación específicos requeridos por la guía.
    """
    errores = {
        "nomina": "Nómina en formato incorrecto. Debe capturar solo números y letras.",
        "nombre": "Nombre de usuario en formato incorrecto. Debe capturar solo letras.",
        "cantidad": "Cantidad de videos en formato incorrecto. Debe capturar solo números.",
        "titulo": "Título del video en formato incorrecto. Debe capturar solo números y letras.",
        "nombre_video": "Nombre del video en formato incorrecto. Debe capturar solo números y letras.",
        "extension": "Extensión del video en formato incorrecto. Debe capturar solo números y letras.",
        "tamano_formato": "Tamaño del video en formato incorrecto. Debe capturar solo números.",
        "tamano_limite": "El archivo no debe pesar más de 3 MB"
    }
    print(f"\n[ERROR] {errores.get(tipo_error, 'Error desconocido.')}\n")

# =====================================================================
# FUNCIONES DE VALIDACIÓN
# =====================================================================
def validar_captura(valor, tipo_validacion):
    """
    Valida las entradas usando expresiones regulares según los criterios solicitados.
    """
    if tipo_validacion == "alfanumerico":
        # Permite letras, números y espacios básicos (útil para títulos)
        return bool(re.match(r"^[A-Za-z0-9\s]+$", valor))
    elif tipo_validacion == "alfabetico":
        # Permite letras y espacios (para nombres propios)
        return bool(re.match(r"^[A-Za-z\s]+$", valor))
    elif tipo_validacion == "numerico":
        # Permite solo dígitos enteros
        return bool(re.match(r"^[0-9]+$", valor))
    return False

# =====================================================================
# FUNCIÓN PARA MANEJO DE EXCEPCIONES Y TAMAÑO
# =====================================================================
def validar_tamano_video(valor_str):
    """
    Maneja excepciones para el tamaño del video (conversión y límites 0-3 MB).
    """
    try:
        # Intenta convertir a número flotante para permitir decimales si es necesario
        tamano = float(valor_str)
    except ValueError:
        # Excepción 1: El usuario introdujo caracteres no numéricos
        mostrar_error("tamano_formato")
        raise ValueError("Formato incorrecto")
        
    # Excepción 2: Validación de rango de tamaño (0 a 3 MB)
    if tamano < 0 or tamano > 3:
        mostrar_error("tamano_limite")
        raise ValueError("Tamaño fuera de rango")
        
    return tamano

# =====================================================================
# FUNCIONES DE CAPTURA PRINCIPALES
# =====================================================================
def pedir_datos_usuario():
    """
    Solicita y valida la información inicial del usuario.
    """
    while True:
        id_usuario = input("Ingrese su ID (número de nómina): ").strip()
        if validar_captura(id_usuario, "alfanumerico"):
            break
        mostrar_error("nomina")

    while True:
        nombre = input("Ingrese su nombre completo: ").strip()
        if validar_captura(nombre, "alfabetico"):
            break
        mostrar_error("nombre")

    while True:
        cantidad_str = input("¿Qué cantidad de videos subirá?: ").strip()
        if validar_captura(cantidad_str, "numerico"):
            cantidad = int(cantidad_str)
            break
        mostrar_error("cantidad")

    return id_usuario, nombre, cantidad

def pedir_datos_videos(n_videos):
    """
    Ciclo iterativo para recopilar los datos de los N videos a subir.
    """
    lista_videos = []
    
    for i in range(1, n_videos + 1):
        print(f"\n--- Captura de datos para el Video {i} de {n_videos} ---")
        
        while True:
            titulo = input(f"Título del video {i}: ").strip()
            if validar_captura(titulo, "alfanumerico"):
                break
            mostrar_error("titulo")
            
        while True:
            nombre_vid = input(f"Nombre del archivo de video {i}: ").strip()
            if validar_captura(nombre_vid, "alfanumerico"):
                break
            mostrar_error("nombre_video")
            
        while True:
            extension = input(f"Extensión del video {i} (ej. mpg, mov, mp4): ").strip()
            # Quitamos el punto inicial si el usuario lo pone por error para evaluar el formato alfanumérico
            ext_limpia = extension.lstrip('.')
            if validar_captura(ext_limpia, "alfanumerico"):
                break
            mostrar_error("extension")
            
        while True:
            tamano_str = input(f"Tamaño del video {i} (en MB, máx 3): ").strip()
            try:
                tamano = validar_tamano_video(tamano_str)
                break
            except ValueError:
                continue # Si ocurre una excepción controlada, repite el bucle de captura de tamaño
                
        # Guardamos los datos del video en un diccionario
        lista_videos.append({
            "titulo": titulo,
            "nombre": nombre_vid,
            "extension": extension if extension.startswith('.') else f".{extension}",
            "tamano": tamano
        })
        
    return lista_videos

# =====================================================================
# FLUJO PRINCIPAL DEL SISTEMA
# =====================================================================
def ejecutar_sistema():
    print("=== BIENVENIDO AL SISTEMA DE STREAMING PRO-GOL WATCH ===")
    
    while True:
        # 1. Captura inicial de datos
        id_usuario, nombre, cantidad = pedir_datos_usuario()
        
        # 2. Confirmación de información
        print(f"\nBienvenido {nombre}, tu número de nómina es {id_usuario} y estás intentando subir {cantidad} videos.")
        confirmacion = input("¿Es correcta la información? (Si/No): ").strip().lower()
        
        if confirmacion in ['si', 'sí']:
            # Captura los N videos usando ciclos
            videos_capturados = pedir_datos_videos(cantidad)
            
            # 3. Formatear y guardar en salida.txt
            # Formato requerido: Nómina | Nombre | Cantidad | Título 1 | Nombre 1 | Extensión 1 | Tamaño 1 | ...
            linea_salida = f"{id_usuario} | {nombre} | {cantidad}"
            for vid in videos_capturados:
                linea_salida += f" | {vid['titulo']} | {vid['nombre']} | {vid['extension']} | {int(vid['tamano'])}"
            linea_salida += " |\n"
            
            try:
                with open("salida.txt", "a", encoding="utf-8") as archivo:
                    archivo.write(linea_salida)
                print("\n[ÉXITO] Datos validados y guardados correctamente en 'salida.txt'.")
            except IOError:
                print("\n[ERROR] No se pudo escribir en el archivo salida.txt.")
                
            break # Termina la ejecución exitosamente
            
        elif confirmacion == 'no':
            # Preguntar si desea salir
            salir = input("¿Desea salir del sistema? (Si/No): ").strip().lower()
            if salir in ['si', 'sí']:
                print("\nMuchas gracias por haber usado nuestro sistema, hasta pronto.")
                sys.exit()
            else:
                print("\nReiniciando captura de datos...\n")
                continue # Vuelve a empezar el ciclo while principal
        else:
            print("\nOpción no válida. Reiniciando flujo por seguridad.")

if __name__ == "__main__":
    ejecutar_sistema()