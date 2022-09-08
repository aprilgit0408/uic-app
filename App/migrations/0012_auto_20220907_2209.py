# Generated by Django 3.2.6 on 2022-09-07 22:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0011_auto_20220830_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='idDocente',
            field=models.CharField(choices=[('2', 'Carlos Guano'), ('5', 'Jeffery Naranjo')], max_length=13, verbose_name='Docente'),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='idEstudiantes',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Listado de Estudiantes'),
        ),
        migrations.AlterField(
            model_name='tribunal',
            name='primerDocente',
            field=models.CharField(choices=[(2, 'Carlos Guano'), (3, 'Katherin Elizabeth Siza Imbaquingo'), (4, 'Erick Josa'), (5, 'Jeffery Naranjo'), (6, 'Pablo Acosta')], max_length=15, verbose_name='Primer Docente'),
        ),
        migrations.AlterField(
            model_name='tribunal',
            name='primerDocenteSuplente',
            field=models.CharField(choices=[(2, 'Carlos Guano'), (3, 'Katherin Elizabeth Siza Imbaquingo'), (4, 'Erick Josa'), (5, 'Jeffery Naranjo'), (6, 'Pablo Acosta')], max_length=15, verbose_name='Primer Docente Suplente'),
        ),
        migrations.AlterField(
            model_name='tribunal',
            name='segundoDocente',
            field=models.CharField(choices=[(2, 'Carlos Guano'), (3, 'Katherin Elizabeth Siza Imbaquingo'), (4, 'Erick Josa'), (5, 'Jeffery Naranjo'), (6, 'Pablo Acosta')], max_length=15, verbose_name='Segundo Docente'),
        ),
        migrations.AlterField(
            model_name='tribunal',
            name='segundoDocenteSuplente',
            field=models.CharField(choices=[(2, 'Carlos Guano'), (3, 'Katherin Elizabeth Siza Imbaquingo'), (4, 'Erick Josa'), (5, 'Jeffery Naranjo'), (6, 'Pablo Acosta')], max_length=15, verbose_name='Segundo Docente Suplente'),
        ),
        migrations.AlterField(
            model_name='tribunal',
            name='terceroDocente',
            field=models.CharField(choices=[(2, 'Carlos Guano'), (3, 'Katherin Elizabeth Siza Imbaquingo'), (4, 'Erick Josa'), (5, 'Jeffery Naranjo'), (6, 'Pablo Acosta')], max_length=15, verbose_name='Tercer Docente'),
        ),
        migrations.AlterField(
            model_name='tribunal',
            name='terceroDocenteSuplente',
            field=models.CharField(choices=[(2, 'Carlos Guano'), (3, 'Katherin Elizabeth Siza Imbaquingo'), (4, 'Erick Josa'), (5, 'Jeffery Naranjo'), (6, 'Pablo Acosta')], max_length=15, verbose_name='Tercer Docente Suplente'),
        ),
        migrations.CreateModel(
            name='Tutoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(verbose_name='Temas a tratarse')),
                ('fecha', models.DateTimeField(verbose_name='Fecha y hora de tutoría')),
                ('archivo', models.FileField(blank=True, null=True, upload_to='tutorias', verbose_name='Archivo de Tutoría')),
                ('idProyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.proyecto', verbose_name='Proyecto')),
            ],
        ),
    ]