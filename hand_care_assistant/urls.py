from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),

    #Registrarse
    path('registro', views.registro, name = 'registro'),

    #Iniciar sesion
    path('iniciar_sesion', views.iniciar_sesion, name = 'iniciar_sesion'),

    #Cerar sesion
    path('cerrar_sesion', views.cerrar_sesion, name = 'cerrar_sesion'),
    
    path('inicio', views.inicio, name = 'inicio'),

    #URLS de pacientes
    #Inicio
    path('pacientes', views.pacientes, name = 'pacientes'),
    #Crear
    path('pacientes/nuevo', views.nuevo_paciente, name = 'nuevo'),
    #Editar
    path('pacientes/editar/<int:id>', views.editar_paciente, name = 'editar'),
    #Eliminar
    path('pacientes/eliminar/<int:id>', views.eiminar_paciente, name='eliminar'),

    #URLs terapias
    path('pacientes/terapias/<int:id>', views.terapias, name = 'terapias'),
]