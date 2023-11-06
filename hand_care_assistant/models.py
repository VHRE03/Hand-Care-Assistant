from django.db import models

# Create your models here.
class Fisioterapeuta(models.Model):
    id_fisioterapeuta = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    especialidad = models.CharField(max_length=50, blank=True, null=True)
    correo_electronico = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    usuario = models.CharField(max_length=10, blank=True, null=True)
    contra = models.CharField(unique=True, max_length=20)

class Paciente(models.Model):
    id_paciente = models.AutoField(primary_key=True)
    id_fisioterapeuta = models.ForeignKey(Fisioterapeuta, models.DO_NOTHING, db_column='id_fisioterapeuta', blank=True, null=True)
    nombre = models.CharField(max_length=50, blank=True, null=True, verbose_name = 'Nombre')
    apellido = models.CharField(max_length=50, blank=True, null=True, verbose_name = 'Apellido')
    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name = 'Fecha de nacimiento')
    correo = models.CharField(max_length=100, blank=True, null=True, verbose_name = 'Correo electrónico')
    telefono = models.CharField(max_length=10, blank=True, null=True, verbose_name = 'Número telefónico')
    direccion = models.CharField(max_length=200, blank=True, null=True, verbose_name = 'Dirección')
    diagnostico_medico = models.TextField(blank=True, null=True, verbose_name = 'Diagnóstico médico')
    fecha_inicio_terapia = models.DateField(blank=True, null=True, verbose_name = 'Fecha de inicio de terapia')
    plan_terapia = models.IntegerField(blank=True, null=True, verbose_name = 'Plan de terapia')
    paciente_activo = models.CharField(max_length=1, blank=True, null=True)

class Terapia(models.Model):
    id_terapia = models.AutoField(primary_key=True)
    id_paciente = models.ForeignKey(Paciente, models.DO_NOTHING, db_column='id_paciente', blank=True, null=True)
    fecha_hora_inicio = models.DateTimeField(blank=True, null=True)
    fecha_hora_fin = models.DateTimeField(blank=True, null=True)
    actividad_realizada = models.CharField(max_length=100, blank=True, null=True)