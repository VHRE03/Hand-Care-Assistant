from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from .models import Fisioterapeuta, Paciente, Terapia
from .forms import Paciente_form
from django.contrib.auth.decorators import login_required

from datetime import datetime
from statistics import mean
from collections import defaultdict
from collections import Counter

#Pagina principal
def home(request):
    return render(request, 'home.html')

#Datos grafica 1
def datos_grafica_1(id_fisioterapeuta):

    pacientes = Paciente.objects.filter(id_fisioterapeuta = id_fisioterapeuta).all()

    fechas_nacimiento = []
    for paciente in pacientes:
        fechas_nacimiento.append(paciente.fecha_nacimiento)

    #Obtiene la fecha actual
    fecha_actual = datetime.now()

    #Calcula la edad de cada paciente
    edades = [fecha_actual.year - fecha.year - ((fecha_actual.month, fecha_actual.day) < (fecha.month, fecha.day)) for fecha in fechas_nacimiento]

    #Crea un diccionario para almacenar el conteo de edades por rango de 10 en 10 años
    conteo_por_rango_edad = {i: 0 for i in range(0, max(edades) + 1, 10)}

    #Itera sobre las edades y cuenta por rango de edad
    for edad in edades:
        rango_edad = (edad // 10) * 10
        conteo_por_rango_edad[rango_edad] += 1

    #Imprime el resultado
    conteo_edades = []
    for rango, conteo in conteo_por_rango_edad.items():
        conteo_edades.append(conteo)

    return conteo_edades

#Datos grafica 2
def datos_grafica_2(id_fisioterapeuta):
    pacientes = Paciente.objects.filter(id_fisioterapeuta = id_fisioterapeuta).all()

    # Crea un diccionario para almacenar el conteo de hombres y mujeres
    conteo_por_genero = {"Masculino": 0, "Femenino": 0, "Otro": 0}

    # Itera sobre la lista de pacientes y cuenta por género
    for paciente in pacientes:
        genero = paciente.sexo
        if genero in conteo_por_genero:
            conteo_por_genero[genero] += 1

    conteo_genero = []
    conteo_genero.append(conteo_por_genero['Masculino'])
    conteo_genero.append(conteo_por_genero['Femenino'])
    conteo_genero.append(conteo_por_genero['Otro'])

    return conteo_genero

#Datos grafica 3
def datos_grafica_3(id_fisioterapeuta):
    pacientes = Paciente.objects.filter(id_fisioterapeuta = id_fisioterapeuta).all()

    fechas_terapia = []
    for paciente in pacientes:
        terapias = Terapia.objects.filter(id_paciente = paciente.id_paciente).all()
        for terapia in terapias:
            fechas_terapia.append(terapia.fecha_hora_fin)

    # Crea un diccionario para almacenar el conteo de fechas por día de la semana
    concurrencia_por_dia = [0] * 7

    # Itera sobre las fechas y cuenta por día de la semana
    for fecha in fechas_terapia:
        dia_de_la_semana = fecha.weekday()  # 0 = lunes, 1 = martes, ..., 6 = domingo
        concurrencia_por_dia[dia_de_la_semana] += 1

    return concurrencia_por_dia

def datos_grafica_4(id_fisioterapeuta):
    pacientes = Paciente.objects.filter(id_fisioterapeuta = id_fisioterapeuta).all()

    fechas_terapia = []
    for paciente in pacientes:
        terapias = Terapia.objects.filter(id_paciente = paciente.id_paciente).all()
        for terapia in terapias:
            fechas_terapia.append(terapia.fecha_hora_fin)

    # Crea un objeto Counter para almacenar la concurrencia de cada mes
    concurrencia_por_mes = Counter()

    # Itera sobre las fechas y cuenta por mes
    for fecha in fechas_terapia:
        mes_del_ano = fecha.month
        concurrencia_por_mes[mes_del_ano] += 1

    # Convierte el resultado en una lista ordenada
    concurrencia_por_mes_lista = [concurrencia_por_mes[mes] for mes in range(1, 13)]

    # Imprime el vector de concurrencia por mes
    return concurrencia_por_mes_lista

@login_required
def inicio(request):

    #Obtenemos el nombre de usuario registrdo
    usuario = request.user

    #Obtenemos el ID del fisioterapeuta relacionado a ese usuario
    id_fisioterapeuta = Fisioterapeuta.objects.filter(usuario = usuario).first().id_fisioterapeuta

    #Obtenemos el fisioterapeuta
    fisioterapeuta = Fisioterapeuta.objects.get(id_fisioterapeuta = id_fisioterapeuta)

    def obtener_datos_generales_1():
        #Datos generales 1
        datos_generales_1 = Paciente.objects.filter(id_fisioterapeuta = id_fisioterapeuta).count()

        return datos_generales_1
        
    def obtener_datos_generales_5():
        #Datos generales 5
        def calcular_edad(fecha_nacimiento):
            # Obtener la fecha actual
            fecha_actual = datetime.now()

            # Convertir la cadena de fecha de nacimiento a objeto datetime
            fecha_nacimiento = fecha_nacimiento

            # Calcular la diferencia entre la fecha actual y la fecha de nacimiento
            edad = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

            return edad
        
        #Obtenemos la lista de los pacientes
        pacientes = Paciente.objects.filter(id_fisioterapeuta = id_fisioterapeuta)

        #Lista de edades
        edades = []

        for paciente in pacientes:
            edades.append(calcular_edad(paciente.fecha_nacimiento))

        datos_generales_5 = round(mean(edades))

        return datos_generales_5

    

    datos = [12, 13, 23, 6, 67, 5]


    return render(request, 'paginas/inicio.html', {
        'nombre_fisioterapeuta': fisioterapeuta.nombre + ' ' + fisioterapeuta.apellido, 
        'datos' : datos,
        'datos_generales_1': obtener_datos_generales_1,
        'datos_generales_5': obtener_datos_generales_5,
        'datos_grafica_1': datos_grafica_1(id_fisioterapeuta),
        'datos_grafica_2': datos_grafica_2(id_fisioterapeuta),
        'datos_grafica_3': datos_grafica_3(id_fisioterapeuta),
        'datos_grafica_4': datos_grafica_4(id_fisioterapeuta)
    })

#Vistas de pacientess
#Inicio
def pacientes(request):

    formulario = Paciente_form(request.POST or None)

    #Obtenemos el nombre de usuario registrdo
    usuario = request.user

    #Obtenemos el ID del fisioterapeuta relacionado a ese usuario
    id_fisioterapeuta = Fisioterapeuta.objects.filter(usuario = usuario).first()

    #Obtenemos la lista de los pacientes del fisioterapeuta 
    pacientes = Paciente.objects.filter(id_fisioterapeuta = id_fisioterapeuta)

    if request.POST:
        #Busqueda por nombre
        pacientes_busqueda = Paciente.objects.filter(nombre__icontains = request.POST['nombre']).all()

        return render(request, 'pacientes/index.html', {'pacientes' : pacientes_busqueda})


    #Mostramos la pagina con los pacientes
    return render(request, 'pacientes/index.html', {'pacientes' : pacientes, 'formulario': formulario, 'id_fisioterapeuta': id_fisioterapeuta})

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
    print(formulario['nombre'])
    return render(request, 'pacientes/crear.html', {'formulario': formulario, 'id_fisioterapeuta': id_fisioterapeuta})

#Editar paciente
def editar_paciente(request, id):

    #Obtenemos el paciente que se quiere editar
    paciente = Paciente.objects.get(id_paciente = id)

    #Creamos el formulario con los valores del paciente seeccionado
    formulario = Paciente_form(request.POST or None, instance = paciente)

    if formulario.is_valid() and request.POST:
        print(request.POST)
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
