# Generated by Django 4.1.1 on 2023-06-17 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0010_alter_proyecto_iddocente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='idDocente',
            field=models.PositiveIntegerField(choices=[], verbose_name='Docente Tutor del Proyecto'),
        ),
    ]