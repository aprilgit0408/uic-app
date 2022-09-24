# Generated by Django 3.2.6 on 2022-09-21 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0008_auto_20220921_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avance',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='documentacion', verbose_name='Documento'),
        ),
        migrations.AlterField(
            model_name='avance',
            name='porcentaje',
            field=models.PositiveIntegerField(blank=True, verbose_name='Porcentaje completado'),
        ),
    ]