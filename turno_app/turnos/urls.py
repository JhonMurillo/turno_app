from django.urls import path
from turnos import views 

urlpatterns = [
    path(
        route='<str:slug_identificador>/',
        view = views.TurnoListView.as_view(),
        name='turnos'
    )
]