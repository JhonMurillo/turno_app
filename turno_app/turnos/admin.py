from django.contrib import admin

# Register your models here.
from turnos.models import Turno, Empresa

admin.site.register(Turno)
admin.site.register(Empresa)
