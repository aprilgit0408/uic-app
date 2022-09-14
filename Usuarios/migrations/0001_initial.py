# Generated by Django 3.2.6 on 2022-09-13 20:42

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0014_auto_20210810_2208'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('abreviatura', models.CharField(choices=[('MSc.', 'MSc.'), ('Mg.', 'Mg.'), ('Mtr.', 'Mtr.'), ('PhD.', 'PhD.')], max_length=8, verbose_name='Abreviatura')),
                ('nombreDirector', models.CharField(max_length=50, verbose_name='Director actual de la Carrera')),
                ('nombre', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Nombre de la Carrera')),
                ('fechaCreacion', models.DateField(auto_now_add=True)),
                ('fechaModificacion', models.DateField(blank=True, editable=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Facultad',
            fields=[
                ('nombre', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Nombre de la Facultad')),
                ('sigla', models.CharField(max_length=20, verbose_name='Nombre corto')),
                ('fechaCreacion', models.DateField(auto_now_add=True)),
                ('fechaModificacion', models.DateField(blank=True, editable=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Nivel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre del Nivel')),
                ('periodoInicio', models.DateField(verbose_name='Periodo de inicio de Proyecto')),
                ('periodoFin', models.DateField(blank=True, null=True, verbose_name='Periodo de fin de Proyecto')),
                ('periodoActual', models.DateField(verbose_name='Periodo Actual')),
            ],
        ),
        migrations.CreateModel(
            name='Perfiles',
            fields=[
                ('nombre', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Perfiles')),
            ],
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='users', verbose_name='Imagen')),
                ('celular', models.CharField(max_length=10, verbose_name='Celular')),
                ('modalidad', models.CharField(blank=True, choices=[('Trabajo de Integración Curricular', 'Trabajo de Integración Curricular'), ('Examen con Carácter Complexivo', 'Examen con Carácter Complexivo')], max_length=50, null=True)),
                ('token', models.CharField(blank=True, editable=False, max_length=36, null=True)),
                ('genero', models.CharField(blank=True, choices=[('Señor', 'Señor'), ('Señora', 'Señora')], max_length=10, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('idCarrera', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Usuarios.carrera', verbose_name='Carrera')),
                ('idNivel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Usuarios.nivel', verbose_name='Nivel')),
                ('perfil', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Usuarios.perfiles', verbose_name='Perfil')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='carrera',
            name='idFacultad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Usuarios.facultad', verbose_name='Facultad'),
        ),
    ]
