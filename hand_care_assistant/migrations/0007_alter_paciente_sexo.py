# Generated by Django 4.2.6 on 2023-11-27 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hand_care_assistant', '0006_alter_paciente_sexo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='sexo',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
