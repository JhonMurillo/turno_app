from django.urls import path
from turnos import views 

urlpatterns = [
    path(
        route='<str:slug_identificador>/',
        view = views.EmpresaDetailView.as_view(),
        name='turnos'
    ),
    path(
        route='<str:slug_identificador>/turno',
        view = views.TurnoCreateView.as_view(),
        name='pedir_turno'
    )
]