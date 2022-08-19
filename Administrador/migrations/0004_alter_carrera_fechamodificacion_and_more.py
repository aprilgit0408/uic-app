# Generated by Django 4.1 on 2022-08-12 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Administrador', '0003_remove_tribunal_primerdocente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrera',
            name='fechaModificacion',
            field=models.DateField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='docente',
            name='fechaModificacion',
            field=models.DateField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='fechaModificacion',
            field=models.DateField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='facultad',
            name='fechaModificacion',
            field=models.DateField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='listaverificacion',
            name='fechaModificacion',
            field=models.DateField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='nivel',
            name='periodoActual',
            field=models.DateField(verbose_name='Periodo Actual'),
        ),
        migrations.AlterField(
            model_name='nivel',
            name='periodoFin',
            field=models.DateField(verbose_name='Periodo de fin de Proyecto'),
        ),
        migrations.AlterField(
            model_name='nivel',
            name='periodoInicio',
            field=models.DateField(verbose_name='Periodo de inicio de Proyecto'),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='fechaModificacion',
            field=models.DateField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='tribunal',
            name='fechaModificacion',
            field=models.DateField(blank=True, editable=False, null=True),
        ),
    ]
