# Generated by Django 3.2.6 on 2022-09-21 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_auto_20220921_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avance',
            name='usuarioModificacion',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='avance',
            name='usuarioRegistro',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='grupoexperto',
            name='usuarioModificacion',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='grupoexperto',
            name='usuarioRegistro',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='listaverificacion',
            name='usuarioModificacion',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='listaverificacion',
            name='usuarioRegistro',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='usuarioModificacion',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='usuarioRegistro',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='tribunal',
            name='usuarioModificacion',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='tribunal',
            name='usuarioRegistro',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='tutoria',
            name='usuarioModificacion',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='tutoria',
            name='usuarioRegistro',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True),
        ),
    ]