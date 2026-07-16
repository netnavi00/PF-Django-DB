import re
import sys

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

# Funcióń auxiliar de validación con Regex
def validar_captura(valor, tipo_validacion):
    if tipo_validacion == "alfanumerico":
        return bool(re.match(r"^[A-Za-z0-9\s]+$", valor))
    elif tipo_validacion == "alfabetico":
        return bool(re.match(r"^[A-Za-z\s]+$", valor))
    elif tipo_validacion == "numerico":
        return bool(re.match(r"^[0-9]+$", valor))
    return False

# =====================================================================
# CLASE PERSONA
# =====================================================================
class Persona:
    def __init__(self):
        # Atributos inicializados vacíos [cite: 161]
        self.nombre = ""
        self.id_nomina = ""

    def capturar_id(self):
        """Solicita y valida el ID (nómina) [cite: 166]"""
        while True:
            valor = input("Ingrese su ID (número de nómina): ").strip()
            if validar_captura(valor, "alfanumerico"):
                self.id_nomina = valor
                break
            mostrar_error("nomina")

    def capturar_nombre(self):
        """Solicita y valida el nombre [cite: 165]"""
        while True:
            valor = input("Ingrese su nombre completo: ").strip()
            if validar_captura(valor, "alfabetico"):
                self.nombre = valor
                break
            mostrar_error("nombre")

    def imprimir_id(self):
        """Retorna o imprime el ID [cite: 168]"""
        return self.id_nomina

    def imprimir_nombre(self):
        """Retorna o imprime el nombre [cite: 167]"""
        return self.nombre


# =====================================================================
# CLASE VIDEOS
# =====================================================================
class Videos:
    def __init__(self):
        # Atributos individuales requeridos [cite: 170]
        self.titulo_video = "" # Usado como identificador/título
        self.nombre_video = ""
        self.extension_video = ""
        self.tamano_video = 0.0

    def capturar_nombre_video(self):
        """Captura el título y el nombre del archivo de video [cite: 175]"""
        # Captura del título (necesario para el formato de salida.txt)
        while True:
            valor_titulo = input("Título del video: ").strip()
            if validar_captura(valor_titulo, "alfanumerico"):
                self.titulo_video = valor_titulo
                break
            mostrar_error("titulo")

        # Captura del nombre del archivo
        while True:
            valor_nombre = input("Nombre del archivo de video: ").strip()
            if validar_captura(valor_nombre, "alfanumerico"):
                self.nombre_video = valor_nombre
                break
            mostrar_error("nombre_video")

    def capturar_la_extension_del_video(self):
        """Captura y valida la extensión [cite: 176]"""
        while True:
            valor = input("Extensión del video (ej. mpg, mov, mp4): ").strip()
            ext_limpia = valor.lstrip('.')
            if validar_captura(ext_limpia, "alfanumerico"):
                self.extension_video = valor if valor.startswith('.') else f".{valor}"
                break
            mostrar_error("extension")

    def capturar_el_tamano_del_video(self):
        """Captura y maneja excepciones del tamaño (0-3 MB) [cite: 177]"""
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
                
            self.tamano_video = tamano
            break

    # Métodos de impresión requeridos [cite: 178, 179]
    def imprimir_nombre_video(self):
        return self.nombre_video

    def imprimir_la_extension_del_video(self):
        return self.extension_video

    def imprimir_el_tamano_del_video(self):
        return self.tamano_video


# =====================================================================
# FLUJO PRINCIPAL DEL SISTEMA (IMPLEMENTANDO POO)
# =====================================================================
def ejecutar_sistema():
    print("=== BIENVENIDO AL SISTEMA DE STREAMING PRO-GOL WATCH (Etapa 2) ===")
    
    while True:
        # Instanciamos el objeto tipo Persona [cite: 180]
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
            
            # Ciclo para capturar cada uno de los N objetos del tipo Videos [cite: 180, 278]
            for i in range(1, cantidad + 1):
                print(f"\n--- Captura de datos para el Video {i} de {cantidad} ---")
                video_obj = Videos() # Creación del objeto [cite: 180]
                video_obj.capturar_nombre_video()
                video_obj.capturar_la_extension_del_video()
                video_obj.capturar_el_tamano_del_video()
                lista_objetos_videos.append(video_obj)
            
            # Construcción de la línea para salida.txt usando los métodos de los objetos [cite: 185]
            linea_salida = f"{usuario.imprimir_id()} | {usuario.imprimir_nombre()} | {cantidad}"
            
            for vid in lista_objetos_videos:
                linea_salida += f" | {vid.titulo_video} | {vid.imprimir_nombre_video()} | {vid.imprimir_la_extension_del_video()} | {int(vid.imprimir_el_tamano_del_video())}"
            linea_salida += " |\n"
            
            # Guardado de la información [cite: 185]
            try:
                with open("salida.txt", "a", encoding="utf-8") as archivo:
                    archivo.write(linea_salida)
                print("\n[ÉXITO] Datos de los objetos guardados correctamente en 'salida.txt'.")
            except IOError:
                print("\n[ERROR] No se pudo escribir en el archivo salida.txt.")
                
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