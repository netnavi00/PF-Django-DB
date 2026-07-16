import os
import sys
import re
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# =====================================================================
# CONFIGURACIÓN DE ENTORNO DJANGO (Permite usar los modelos fuera del servidor web)
# =====================================================================
# Establece el módulo de configuración del proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mis_videos.settings')
# Inicializa Django
django.setup()

# Importamos los modelos de la aplicación 'streaming' una vez configurado Django
from streaming.models import TBL_Usuario, TBL_Video, TBL_Usuario_Video

# =====================================================================
# FUNCIÓN ÚNICA PARA MOSTRAR MENSAJES DE ERROR
# =====================================================================
def mostrar_error(tipo_error):
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

# Función auxiliar de validación con Regex
def validar_captura(valor, tipo_validacion):
    if tipo_validacion == "alfanumerico":
        return bool(re.match(r"^[A-Za-z0-9\s]+$", valor))
    elif tipo_validacion == "alfabetico":
        return bool(re.match(r"^[A-Za-z\s]+$", valor))
    elif tipo_validacion == "numerico":
        return bool(re.match(r"^[0-9]+$", valor))
    return False

# =====================================================================
# CLASE PERSONA (Adaptada para interactuar con la Base de Datos)
# =====================================================================
class Persona:
    def __init__(self):
        self.nombre = ""
        self.id_nomina = ""

    def capturar_id(self):
        """Solicita y valida el ID (nómina)"""
        while True:
            valor = input("Ingrese su ID (número de nómina): ").strip()
            if validar_captura(valor, "alfanumerico"):
                self.id_nomina = valor
                break
            mostrar_error("nomina")

    def capturar_nombre(self):
        """Solicita y valida el nombre"""
        while True:
            valor = input("Ingrese su nombre completo: ").strip()
            if validar_captura(valor, "alfabetico"):
                self.nombre = valor
                break
            mostrar_error("nombre")

    def imprimir_id(self):
        return self.id_nomina

    def imprimir_nombre(self):
        return self.nombre

    def guardar_en_db(self):
        """
        Guarda o actualiza el usuario en la tabla TBL_Usuario.
        Usa update_or_create para evitar duplicados si la nómina ya existe.
        """
        usuario_db, created = TBL_Usuario.objects.update_or_create(
            id_nomina=self.id_nomina,
            defaults={'nombre': self.nombre}
        )
        return usuario_db


# =====================================================================
# CLASE VIDEOS (Adaptada para interactuar con la Base de Datos)
# =====================================================================
class Videos:
    def __init__(self):
        self.titulo_video = ""
        self.nombre_video = ""
        self.extension_video = ""
        self.tamano_video = 0

    def capturar_nombre_video(self):
        """Captura el título y el nombre del archivo de video"""
        while True:
            valor_titulo = input("Título del video: ").strip()
            if validar_captura(valor_titulo, "alfanumerico"):
                self.titulo_video = valor_titulo
                break
            mostrar_error("titulo")

        while True:
            valor_nombre = input("Nombre del archivo de video: ").strip()
            if validar_captura(valor_nombre, "alfanumerico"):
                self.nombre_video = valor_nombre
                break
            mostrar_error("nombre_video")

    def capturar_la_extension_del_video(self):
        """Captura y valida la extensión"""
        while True:
            valor = input("Extensión del video (ej. mpg, mov, mp4): ").strip()
            ext_limpia = valor.lstrip('.')
            if validar_captura(ext_limpia, "alfanumerico"):
                self.extension_video = valor if valor.startswith('.') else f".{valor}"
                break
            mostrar_error("extension")

    def capturar_el_tamano_del_video(self):
        """Captura y maneja excepciones del tamaño (0-3 MB)"""
        while True:
            valor_str = input("Tamaño del video (en MB, máx 3): ").strip()
            try:
                tamano = float(valor_str)
            except ValueError:
                mostrar_error("tamano_formato")
                continue
                
            if tamano < 0 or tamano > 3:
                mostrar_error("tamano_limite")
                continue
                
            # Guardamos el tamaño como entero (puedes multiplicarlo si deseas guardarlo en bytes, o guardarlo tal cual)
            self.tamano_video = int(tamano)
            break

    def imprimir_nombre_video(self):
        return self.nombre_video

    def imprimir_la_extension_del_video(self):
        return self.extension_video

    def imprimir_el_tamano_del_video(self):
        return self.tamano_video

    def guardar_en_db(self):
        """
        Guarda el video en la tabla TBL_Video.
        """
        # Creamos una nueva entrada para cada video subido
        video_db = TBL_Video.objects.create(
            nombre=self.nombre_video,
            extension=self.extension_video,
            tamano=self.tamano_video
        )
        return video_db


# =====================================================================
# FLUJO PRINCIPAL DEL SISTEMA (INTERACCIÓN CON ORM DJANGO)
# =====================================================================
def ejecutar_sistema():
    print("=== BIENVENIDO AL SISTEMA DE STREAMING PRO-GOL WATCH (Etapa 3) ===")
    
    while True:
        # Instanciamos el objeto tipo Persona
        usuario = Persona()
        usuario.capturar_id()
        usuario.capturar_nombre()
        
        # Validamos la cantidad de videos de forma local para controlar el ciclo
        while True:
            cantidad_str = input("¿Qué cantidad de videos subirá?: ").strip()
            if validar_captura(cantidad_str, "numerico"):
                cantidad = int(cantidad_str)
                break
            mostrar_error("cantidad")
        
        # Confirmación de los datos en pantalla
        print(f"\nBienvenido {usuario.imprimir_nombre()}, tu número de nómina es {usuario.imprimir_id()} y estás intentando subir {cantidad} videos.")
        confirmacion = input("¿Es correcta la información? (Si/No): ").strip().lower()
        
        if confirmacion in ['si', 'sí']:
            lista_objetos_videos = []
            
            # Ciclo para capturar cada uno de los N objetos del tipo Videos
            for i in range(1, cantidad + 1):
                print(f"\n--- Captura de datos para el Video {i} de {cantidad} ---")
                video_obj = Videos()
                video_obj.capturar_nombre_video()
                video_obj.capturar_la_extension_del_video()
                video_obj.capturar_el_tamano_del_video()
                lista_objects_videos = lista_objetos_videos.append(video_obj)
            
            # -----------------------------------------------------------------
            # GUARDADO DE DATOS EN POSTGRESQL USANDO EL ORM DE DJANGO
            # -----------------------------------------------------------------
            try:
                # 1. Guardar o recuperar usuario
                usuario_db = usuario.guardar_en_db()
                
                # 2. Guardar videos y asociarlos con el usuario
                for video_obj in lista_objetos_videos:
                    # Guardamos el video en la base de datos
                    video_db = video_obj.guardar_en_db()
                    
                    # Creamos la relación intermedia
                    TBL_Usuario_Video.objects.create(
                        id_usuario=usuario_db,
                        id_video=video_db
                    )
                
                print("\n[ÉXITO] Toda la información ha sido almacenada correctamente en PostgreSQL (Base de datos: Pro_Gol).")
            except Exception as e:
                print(f"\n[ERROR] Ocurrió un problema al guardar en la base de datos: {e}")
                
            break
            
        elif confirmacion == 'no':
            salir = input("¿Desea salir del sistema? (Si/No): ").strip().lower()
            if salir in ['si', 'sí']:
                print("\nMuchas gracias por haber usado nuestro sistema, hasta pronto.")
                sys.exit()
            else:
                print("\nReiniciando captura de datos...\n")
                continue
        else:
            print("\nOpción no válida. Reiniciando flujo por seguridad.")

if __name__ == "__main__":
    ejecutar_sistema()