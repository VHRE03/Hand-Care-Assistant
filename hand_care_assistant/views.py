from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from .models import Fisioterapeuta, Paciente, Terapia
from .forms import Paciente_form
from django.contrib.auth.decorators import login_required

#Pagina principal
def home(request):
    return render(request, 'home.html')

# Create your views here.
@login_required
def inicio(request):
    return render(request, 'paginas/inicio.html')

#Vistas de pacientess
#Inicio
def pacientes(request):

    #Obtenemos el nombre de usuario registrdo
    usuario = request.user

    #Obtenemos el ID del fisioterapeuta relacionado a ese usuario
    id_fisioterapeuta = Fisioterapeuta.objects.filter(usuario = usuario).first().id_fisioterapeuta

    #Obtenemos la lista de los pacientes del fisioterapeuta 
    pacientes = Paciente.objects.filter(id_fisioterapeuta = id_fisioterapeuta)

    if request.POST:
        #Busqueda por nombre
        pacientes_busqueda = Paciente.objects.filter(nombre__icontains = request.POST['nombre'])

        return render(request, 'pacientes/index.html', {'pacientes' : pacientes_busqueda})


    #Mostramos la pagina con los pacientes
    return render(request, 'pacientes/index.html', {'pacientes' : pacientes})

#Nuevo paciente
def nuevo_paciente(request):

    formulario = Paciente_form(request.POST or None)

    if formulario.is_valid():

        formulario.save()

        return redirect('pacientes')

    #Obtenemos el nombre de usuario registrdo
    usuario = request.user

    #Obtenemos el ID del fisioterapeuta relacionado a ese usuario
    id_fisioterapeuta = Fisioterapeuta.objects.filter(usuario = usuario).first().id_fisioterapeuta

    return render(request, 'pacientes/crear.html', {'formulario': formulario, 'id_fisioterapeuta': id_fisioterapeuta})

#Editar paciente
def editar_paciente(request, id):

    #Obtenemos el paciente que se quiere editar
    paciente = Paciente.objects.get(id_paciente = id)

    #Creamos el formulario con los valores del paciente seeccionado
    formulario = Paciente_form(request.POST or None, instance = paciente)

    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('pacientes')

    #Mostramos la seccion de editar
    return render(request, 'pacientes/editar.html', {'formulario': formulario, 'id_fisioterapeuta': paciente.id_fisioterapeuta.id_fisioterapeuta })


#Eliminar paciente
def eiminar_paciente(request, id):
    paciente = Paciente.objects.get(id_paciente = id)
    paciente.delete()

    return redirect('pacientes')

#Función para iniciar sesion
def iniciar_sesion(request):

    #Si el metodo es GET se muestra la pagina de inicio de sesion
    if request.method == 'GET':

        return render(request, 'paginas/iniciar_sesion.html')
    
    else:
        #Si el metodo es POST se obtiene los datos ingresados para iniciar sesion

        #Se autentica el usuario y contraseña ingresados
        user = authenticate(request, username = request.POST['nombre_usuario'], password = request.POST['password'])
        
        #Si el usuario no existe o no coincide se muestra un error
        #Si el usuario existe crea una sesion y se redirecciona a la pagina principal
        if user is None:
            return render(request, 'paginas/iniciar_sesion.html', {
                'error': 'Nombre de usuario o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('inicio')

def cerrar_sesion(request):

    logout(request)

    return redirect('iniciar_sesion')

def registro(request):

    if request.method == 'GET':
        return render(request, 'registro.html', {
            'formulario': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:

            try:
                user = User.objects.create_user(username = request.POST['username'], password = request.POST['password1'])

                user.save()

                login(request, user)

                return redirect('inicio')
            except:
                return HttpResponse('El usuario ya existe')
            
        else:
            return HttpResponse('Contraseñas no coinciden')


def terapias(request, id):

    paciente = Paciente.objects.get(id_paciente = id)

    terapias = Terapia.objects.filter(id_paciente = paciente.id_paciente)

    return render(request, 'terapias/index.html', {'paciente': paciente ,'terapias': terapias})
