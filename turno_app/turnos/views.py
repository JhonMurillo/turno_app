# Django
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth import views as auth_views
# from django.urls import reverse, reverse_lazy
# from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from datetime import datetime
from utils.utilidades import groupby_queryset_with_fields

from turnos.models import Turno


class TurnoListView(ListView):

    template_name = 'turnos/visor.html'

    def get_queryset(self):
        slug_identificador = self.kwargs['slug_identificador']
        current_date = datetime.now()
        self.turnos = Turno.objects.filter(
            empresa__slug_identificador__iexact=slug_identificador,
            fecha = current_date,
            estado__in = ['PENDIENTE', 'EN_PROGRESO']
            ).order_by('-secuencia')

        grouped_data = groupby_queryset_with_fields(self.turnos, ['asesor__username'])
        self.turnos_organizados = []
        for row in grouped_data['asesor__username']:
            turno_en_progreso = {
                'secuencia' : '--'
            }
            turno_final = {
                'secuencia' : '--'
            }
            for idx, turno in  enumerate(row['list']):
                asesor = turno.asesor
                # print(turno.estado, turno.secuencia, turno.asesor, len(row['list']))
                if turno.estado == 'EN_PROGRESO':
                    turno_en_progreso = turno
                elif turno.estado == 'PENDIENTE' and idx == len(row['list']) - 1:
                    turno_final = turno
            

            self.turnos_organizados.append({'asesor':asesor , 'turno_en_progreso': turno_en_progreso, 'turno_final' :turno_final})



        return self.turnos_organizados


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['turnos'] = self.turnos_organizados
        return context