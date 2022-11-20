# Generated by Django 4.1.1 on 2022-11-20 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_nombrearchivolistaverificacion_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nombrearchivolistaverificacion',
            name='orden',
        ),
        migrations.AlterField(
            model_name='nombrearchivolistaverificacion',
            name='tipo',
            field=models.PositiveIntegerField(choices=[(1, 'Trabajo de Integración Curricular (TIC)'), (2, 'Examen con Carácter Complexivo (ECC)')], default=1, verbose_name='Modalidad'),
        ),
    ]
