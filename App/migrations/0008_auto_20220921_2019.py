# Generated by Django 3.2.6 on 2022-09-21 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_alter_proyecto_iddocente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avance',
            name='observacion',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Observacion'),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='idDocente',
            field=models.CharField(choices=[('3', 'Carlitos Guano'), ('5', 'Jeffery Naranjo'), ('7', 'Marco Yandun'), ('12', 'Jorge Miranda'), ('13', 'Samuel Lascano'), ('16', 'Milton Del Hierro'), ('17', 'Luis Patiño'), ('18', 'Luis Sanipatin'), ('19', 'Freddy Quinde'), ('20', 'Felix Paguay')], max_length=13, verbose_name='Docente'),
        ),
    ]