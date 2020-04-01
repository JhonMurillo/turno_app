from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from utils.utilidades import groupby_queryset_with_fields
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.urls import reverse_lazy

# Create your models here.

class Empresa(models.Model):

    DEMO='DEMO'
    FULL='FULL'
    LICENCIAS = (
        (DEMO, 'Demostracion'),
        (FULL, 'Full Licencia'),
    )

    nombre = models.CharField(max_length=125)
    slug_identificador = models.SlugField(max_length=20, default='test')
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

    # override the save method to have slug automatically generated
    def save(self, *args, **kwargs):
        self.slug_identificador = slugify(self.slug_identificador).replace('-', '')
        super(Empresa, self).save(*args, **kwargs)

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
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['asesor', 'secuencia', 'fecha'], name='turno_unico')
            # models.UniqueConstraint(fields=['asesor', 'estado', 'fecha'], name='turno_unico_en_progreso')
        ]

    # def get_absolute_url(self):
    #     return reverse_lazy('turnos:pedir_turno')

    def __str__(self):
        return '{asesor} - {secuencia} - {fecha} - {empresa}'.format(
            asesor=self.asesor.get_full_name(), 
            secuencia=self.secuencia, 
            fecha=self.fecha, 
            empresa=self.empresa.nombre
            )

    def get_turnos(slug_identificador):
        current_date = datetime.now()
        turnos = Turno.objects.filter(
            empresa__slug_identificador__iexact=slug_identificador,
            fecha = current_date,
            estado__in = ['PENDIENTE', 'EN_PROGRESO']
            ).order_by('-secuencia')

        grouped_data = groupby_queryset_with_fields(turnos, ['asesor__username'])
        turnos_organizados = []
        for row in grouped_data['asesor__username']:
            turno_en_progreso = {
                'secuencia' : '--'
            }
            turno_final = {
                'secuencia' : '--'
            }
            for idx, turno in  enumerate(row['list']):
                asesor_name = str(turno.asesor.get_full_name())
                # print(turno.estado, turno.secuencia, turno.asesor, len(row['list']))
                if turno.estado == 'EN_PROGRESO':
                    turno_en_progreso = {
                        'secuencia' : turno.secuencia
                    }
                elif turno.estado == 'PENDIENTE' and idx == len(row['list']) - 1:
                    turno_final = {
                        'secuencia' : turno.secuencia
                    }
            turnos_organizados.append({'asesor_name':asesor_name , 'turno_en_progreso': turno_en_progreso, 'turno_final' :turno_final})
        return turnos_organizados


@receiver(post_save, sender=Turno, dispatch_uid="send_new_turnos")
def send_new_turnos(sender, instance, **kwargs):

    print('Sending turnos...')
    turnos_organizados = Turno.get_turnos(instance.empresa.slug_identificador)
    channel_layer = get_channel_layer()
    # Send message to group
    async_to_sync(channel_layer.group_send)(
        instance.empresa.slug_identificador,
        {
        'type': 'send_turnos',
        'turnos_organizados': turnos_organizados
        }
    )