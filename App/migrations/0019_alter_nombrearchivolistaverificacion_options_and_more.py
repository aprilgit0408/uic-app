# Generated by Django 4.1.1 on 2023-12-07 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0018_alter_proyecto_iddocente'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nombrearchivolistaverificacion',
            options={'ordering': ['pk', 'orden']},
        ),
        migrations.AddField(
            model_name='nombrearchivolistaverificacion',
            name='orden',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
