# 🎬 Proyecto Final - Plataforma Streaming (Django + PostgreSQL)

Este repositorio contiene el desarrollo modular de los 4 Avances para la gestión de una plataforma de streaming de video.
---

## 📁 Estructura del Proyecto
``` text
El proyecto está organizado en 4 entregas independientes dentro del mismo directorio raíz:

Proyecto Final/
│
├── Avance_1/              # Etapa 1: POO Básica e Interfaz en Consola
├── Avance_2/              # Etapa 2: Estructuras Complementada de Etapa 1 y Gestión de Errores
├── Avance_3/              # Etapa 3: Integración Django + PostgreSQL (Consola)
├── Avance_4/              # Etapa 4: Frontend Web (HTML/CSS), Validaciones y Forms
│
├── .env.example           # Plantilla de variables de entorno
├── .gitignore              # Archivos excluidos del control de versiones
├── respaldo_db.sql        # Exportación/Respaldo de la base de datos PostgreSQL
└── README.md              # Documentación general del proyecto

```

### 🛠️ Tecnologías Utilizadas
Lenguaje: Python 3.12+

Framework Web: Django 6.0.7

Base de Datos: PostgreSQL 16 (vía psycopg2 / psycopg)

Gestor de BD: pgAdmin 4

Seguridad: python-dotenv para manejo de variables de entorno

Control de Versiones: Git & GitHub

#### ⚙️ Configuración e Instalación Local

1. Clonar el repositorio
git clone https://github.com/netnavi00/PF-Django-DB
cd "Proyecto Final"

2. Crear y activar entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

3. Instalar dependencias
pip install django psycopg2-binary python-dotenv

4. Variables de Entorno (.env)
DB_NAME=Pro_Gol
DB_USER=postgres
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=tu_django_secret_key

##### 🚀 Ejecución del Proyecto (Avance 4 - Web)

Para poner en marcha la interfaz web:

# 1. Navegar a la carpeta del proyecto Django
cd Avance_4/mis_videos

# 2. Ejecutar el servidor de desarrollo
python manage.py runserver

Abre tu navegador e ingresa a: http://127.0.0.1:8000/ o el puerto que marque en terminal.

###### 📌 Resumen de Avances
Avance 1: Modelado de clases POO (Usuario, Video) y menú interactivo en consola.

Avance 2: Métodos CRUD, listas/diccionarios dinámicos y manejo de excepciones.

Avance 3: Mapeo Objeto-Relacional en Django y persistencia física en PostgreSQL.

Avance 4: Interfaz de usuario basada en plantillas HTML/CSS, validaciones con JavaScript y persistencia desde formularios web.