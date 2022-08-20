# Generated by Django 3.2.6 on 2022-08-20 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_auto_20220820_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrera',
            name='fechaCreacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='docente',
            name='fechaCreacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='fechaCreacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='facultad',
            name='fechaCreacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='listaverificacion',
            name='fechaCreacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='fechaCreacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='tribunal',
            name='fechaCreacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
