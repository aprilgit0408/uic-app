# Generated by Django 4.1.1 on 2023-04-23 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0002_remove_nivel_periodoactual_remove_nivel_periodofin_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documento',
            name='idPerfiles',
        ),
        migrations.RemoveField(
            model_name='seguimientodocumentacion',
            name='idDocumento',
        ),
        migrations.DeleteModel(
            name='GrupoExperto',
        ),
    ]