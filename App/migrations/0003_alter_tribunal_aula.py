# Generated by Django 4.1.1 on 2022-10-12 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_docentessuplente_tribunal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tribunal',
            name='aula',
            field=models.CharField(max_length=20, verbose_name='Aula de defensa asignada'),
        ),
    ]
