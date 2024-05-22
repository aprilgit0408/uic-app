# Generated by Django 4.1.1 on 2024-05-21 21:11

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0001_initial'),
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListaValidacionCarrera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaCreacion', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('fechaModificacion', models.DateTimeField(blank=True, editable=False, null=True)),
                ('usuarioRegistro', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('usuarioModificacion', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('visulizacionCompleta', models.BooleanField(default=True)),
                ('nombreCarrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Usuarios.carrera')),
                ('nombreListaVer', models.ManyToManyField(to='App.nombrearchivolistaverificacion')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
