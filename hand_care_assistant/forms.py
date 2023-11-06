from django import forms
from .models import Paciente

class Paciente_form(forms.ModelForm):
    class Meta:
        model = Paciente
        #fields = ['nombre', 'apellido', 'fecha_nacimiento', 'correo', 'telefono', 'direccion', 'diagnostico_medico', 'fecha_inicio_terapia', 'plan_terapia']
        fields = '__all__'