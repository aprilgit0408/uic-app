# Generated by Django 3.2.6 on 2022-09-21 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0006_auto_20220921_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='idDocente',
            field=models.CharField(choices=[], max_length=13, verbose_name='Docente'),
        ),
    ]