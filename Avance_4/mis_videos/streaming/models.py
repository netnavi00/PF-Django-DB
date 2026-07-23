from django.db import models
from django.core.validators import FileExtensionValidator

# a. Tabla para guardar los datos del usuario
class TBL_Usuario(models.Model):
    # Campo llave, alfanumérico de 10 caracteres
    id_nomina = models.CharField(max_length=10, primary_key=True, db_column='id_nomina') 
    # Nombre alfanumérico de 50 caracteres
    nombre = models.CharField(max_length=50)

    class Meta:
        ordering = ['-id_nomina']
        verbose_name = 'TBL_Usuario'     
        verbose_name_plural = 'TBL_Usuarios' 

    def __str__(self):
        return f"{self.id_nomina} - {self.nombre}"

# b. Tabla para guardar videos
class TBL_Video(models.Model):
    # Id del video (Llave primaria autoincrementable)
    id_video = models.AutoField(primary_key=True) 
    # Nombre del video alfanumérico de 50 caracteres
    nombre = models.CharField(max_length=50) 
    # Extensión del video alfanumérico de 5 caracteres
    extension = models.CharField(max_length=5) 
    # Tamaño del video numérico
    tamano = models.IntegerField() 
    # Guarda el arhcivo de video
    archivo = models.FileField(
        upload_to='videos/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov', 'mkv', 'webm'])] # <- Restricción
    )
    class Meta:
        ordering = ['-id_video']
        verbose_name = 'TBL_Video'     
        verbose_name_plural = 'TBL_Videos'

    def __str__(self):
        return self.nombre

# c. Tabla para guardar los videos que subirá el usuario (relación intermedia)
class TBL_Usuario_Video(models.Model):
    # Id del usuario vinculado ,como llave foránea a TBL_Usuario
    id_usuario = models.ForeignKey(TBL_Usuario, on_delete=models.CASCADE, db_column='id_usuario') 
    # Id del video vinculado como llave foránea a TBL_Video
    id_video = models.ForeignKey(TBL_Video, on_delete=models.CASCADE, db_column='id_video') 

    class Meta:
        ordering = ['-id']  # Si esta tabla usa el ID por defecto de Django, esto la ordena también de reciente a antiguo
        verbose_name = 'TBL_Usuario_Video'     
        verbose_name_plural = 'TBL_Usuarios_Videos'

    def __str__(self):
        # Si esta es la tabla que ves en el Admin y solo quieres ver el nombre del video:
        return self.id_video.nombre
    