# Django
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth import views as auth_views
# from django.urls import reverse, reverse_lazy
# from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from datetime import datetime

from turnos.models import Turno, Empresa
from users.models import Profile
from turnos.forms import TurnoForm


class EmpresaDetailView(DetailView):

    template_name = 'turnos/visor.html'
    slug_field = 'slug_identificador'
    slug_url_kwarg = 'slug_identificador'
    queryset = Empresa.objects.filter(activo=True)
    context_object_name = 'empresa'


class TurnoCreateView(SuccessMessageMixin,CreateView):

    template_name  = 'turnos/pedir_turno.html'
    slug_field = 'slug_identificador'
    slug_url_kwarg = 'slug_identificador'
    model = Turno
    fields = ['asesor', 'cliente']
    # success_message = 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug_identificador = self.kwargs['slug_identificador']
        context['asesores'] = Profile.objects.filter(empresa__slug_identificador=slug_identificador)
        context['empresa'] = get_object_or_404(Empresa, slug_identificador=slug_identificador, activo=True)
        context['slug_identificador'] = slug_identificador
        return context


    def form_valid(self, form):
        if form.is_valid:
            
            empresa = get_object_or_404(Empresa, slug_identificador=self.kwargs['slug_identificador'], activo=True)
            form.instance.empresa = empresa
            
            profile = Profile.objects.get(id=self.request.POST['asesor'])
            form.instance.profile = profile
            form.instance.asesor = profile.user

            current_date = datetime.now()
            secuencia = Turno.objects.filter(
                empresa__slug_identificador__iexact=self.kwargs['slug_identificador'],
                asesor__id=profile.user.id,
                profile__id=profile.id,
                fecha = current_date,
            ).count()
            secuencia =  secuencia + 1
            form.instance.secuencia = secuencia
            
            form.save()

            messages.success(self.request, '{} {}'.format(secuencia, profile.user.get_full_name()))

            return super(TurnoCreateView, self).form_valid(form)


    def get_success_url(self):
        return reverse('turnos:pedir_turno', kwargs={'slug_identificador': self.kwargs['slug_identificador']})