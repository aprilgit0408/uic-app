# Generated by Django 4.1.1 on 2024-06-17 21:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Usuarios', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DocentesSuplente',
            fields=[
                ('fechaCreacion', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('fechaModificacion', models.DateTimeField(blank=True, editable=False, null=True)),
                ('usuarioRegistro', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('usuarioModificacion', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('uuID', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('docentesSuplentes', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Docentes Principales')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NombreArchivoListaVerificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaCreacion', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('fechaModificacion', models.DateTimeField(blank=True, editable=False, null=True)),
                ('usuarioRegistro', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('usuarioModificacion', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('orden', models.PositiveIntegerField(blank=True, null=True)),
                ('tipo', models.PositiveIntegerField(choices=[(1, 'Trabajo de Integración Curricular (TIC)'), (2, 'Examen con Carácter Complexivo (ECC)')], default=1, verbose_name='Modalidad')),
            ],
            options={
                'ordering': ['orden'],
            },
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaCreacion', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('fechaModificacion', models.DateTimeField(blank=True, editable=False, null=True)),
                ('usuarioRegistro', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('usuarioModificacion', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre del Proyecto')),
                ('idDocente', models.PositiveIntegerField(verbose_name='Docente Tutor del Proyecto')),
                ('defensa', models.BooleanField(default=False, verbose_name='Proyecto listo para pre/defensa')),
                ('idCarrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Usuarios.carrera', verbose_name='Carrera')),
                ('idEstudiantes', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Listado de Estudiantes')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tutoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaCreacion', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('fechaModificacion', models.DateTimeField(blank=True, editable=False, null=True)),
                ('usuarioRegistro', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('usuarioModificacion', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('descripcion', models.TextField(verbose_name='Temas a tratarse')),
                ('fechaTutoria', models.DateTimeField(verbose_name='Fecha y hora de tutoría')),
                ('archivo', models.FileField(blank=True, null=True, upload_to='tutorias', verbose_name='Archivo de Tutoría')),
                ('idProyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.proyecto', verbose_name='Proyecto')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tribunal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaCreacion', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('fechaModificacion', models.DateTimeField(blank=True, editable=False, null=True)),
                ('usuarioRegistro', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('usuarioModificacion', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('fechaDefensa', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('aula', models.CharField(choices=[('1', 'Aula 1'), ('2', 'Aula 2'), ('3', 'Aula 3'), ('4', 'Aula 4'), ('5', 'Aula 5'), ('6', 'Aula 6'), ('7', 'Aula 7'), ('8', 'Aula 8'), ('9', 'Aula 9')], max_length=20, verbose_name='Aula de defensa asignada')),
                ('docentesPrincipales', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Docentes Principales')),
                ('docentesSuplentes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.docentessuplente', verbose_name='Docentes Principales')),
                ('idProyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.proyecto', verbose_name='Proyecto')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ListaVerificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaCreacion', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('fechaModificacion', models.DateTimeField(blank=True, editable=False, null=True)),
                ('usuarioRegistro', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('usuarioModificacion', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('archivo', models.FileField(upload_to='listaVerificacion', verbose_name='Archivo')),
                ('observacion', models.TextField(blank=True, max_length=100, null=True, verbose_name='Observación')),
                ('estado', models.BooleanField(default=False, verbose_name='Cumplimiento')),
                ('idEstudiante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('idProyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.proyecto', verbose_name='Proyecto')),
                ('nombre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.nombrearchivolistaverificacion', verbose_name='Nombre del Archivo')),
            ],
            options={
                'abstract': False,
            },
        ),
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
                ('nombreListaVer', models.ManyToManyField(blank=True, to='App.nombrearchivolistaverificacion')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Avance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaCreacion', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('fechaModificacion', models.DateTimeField(blank=True, editable=False, null=True)),
                ('usuarioRegistro', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('usuarioModificacion', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('nombreAvance', models.CharField(max_length=100, verbose_name='Nombre Avance')),
                ('observacion', models.CharField(blank=True, max_length=100, null=True, verbose_name='Observacion')),
                ('porcentaje', models.PositiveIntegerField(default=0, verbose_name='Porcentaje completado')),
                ('archivo', models.FileField(blank=True, null=True, upload_to='documentacion', verbose_name='Documento')),
                ('fechaEntrega', models.DateTimeField(default=django.utils.timezone.now)),
                ('idProyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.proyecto', verbose_name='Proyecto')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
