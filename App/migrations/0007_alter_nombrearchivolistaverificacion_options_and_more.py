# Generated by Django 4.1.1 on 2022-11-20 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0006_remove_nombrearchivolistaverificacion_orden_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nombrearchivolistaverificacion',
            options={'ordering': ['pk', 'nombre']},
        ),
        migrations.RenameField(
            model_name='listaverificacion',
            old_name='cumplimiento',
            new_name='estado',
        ),
    ]
