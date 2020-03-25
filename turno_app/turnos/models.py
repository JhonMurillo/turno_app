from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Empresa(models.Model):

    DEMO='DEMO'
    FULL='FULL'
    LICENCIAS = (
        (DEMO, 'Demostracion'),
        (FULL, 'Full Licencia'),
    )

    nombre = models.CharField(max_length=125)
    slug_identificador = models.SlugField(max_length=20, default='TEST')
    telefono = models.CharField(max_length=10)
    email = models.EmailField(max_length=125, blank=True)
    pagina_web = models.URLField(max_length=125, blank=True)
    direccion = models.TextField(max_length=500, blank=True)
    licencia = models.CharField(max_length=100, choices=LICENCIAS, default=DEMO)
    fecha_inicio_demo = models.DateTimeField(blank=True, null=True)
    fecha_fin_demo = models.DateTimeField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Turno(models.Model):

    PENDIENTE='PENDIENTE'
    EN_PROGRESO='EN_PROGRESO'
    FINALIZADO='FINALIZADO'
    ESTADOS = (
        (PENDIENTE, 'Pendiente'),
        (EN_PROGRESO, 'En Progreso'),
        (FINALIZADO, 'Finalizado')
    )

    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE)
    asesor = models.ForeignKey(User,on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile',on_delete=models.CASCADE)
    cliente = models.CharField(max_length=125)
    secuencia = models.PositiveIntegerField(default=1)
    estado = models.CharField(max_length=100, choices=ESTADOS, default=PENDIENTE)
    fecha = models.DateField(auto_now_add=True)
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{asesor} - {secuencia} - {fecha}'.format(asesor=self.asesor, secuencia=self.secuencia, fecha=self.fecha)