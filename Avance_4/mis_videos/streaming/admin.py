from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import TBL_Usuario, TBL_Video, TBL_Usuario_Video

# Registrar modelos para que aparezcan en /admin
admin.site.register(TBL_Usuario)
admin.site.register(TBL_Video)
admin.site.register(TBL_Usuario_Video)