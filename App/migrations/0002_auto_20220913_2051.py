# Generated by Django 3.2.6 on 2022-09-13 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='informacion',
            name='imagen',
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='idDocente',
            field=models.CharField(choices=[('3', 'Carlitos Guano'), ('5', 'Jeffery Naranjo'), ('7', 'Marco Yandun'), ('12', 'Jorge Miranda'), ('13', 'Samuel Lascano'), ('16', 'Milton Del Hierro'), ('17', 'Luis Patiño'), ('18', 'Luis Sanipatin'), ('19', 'Freddy Quinde'), ('20', 'Felix Paguay')], max_length=13, verbose_name='Docente'),
        ),
        migrations.AlterField(
            model_name='tribunal',
            name='primerDocente',
            field=models.CharField(choices=[(2, 'Georgina Arcos'), (3, 'Carlitos Guano'), (4, 'Katherin Siza'), (5, 'Jeffery Naranjo'), (6, 'Morillo Reynaldo'), (7, 'Marco Yandun'), (8, 'Genoveva Chulde'), (9, 'Kevin Lopez'), (10, 'Kelly Mora'), (11, 'Patricio Narvaez'), (12, 'Jorge Miranda'), (13, 'Samuel Lascano'), (14, 'Andy Mauricio Lopez'), (15, 'JENNIFER BERENICE BOLAÑOS GUERRON'), (16, 'Milton Del Hierro'), (17, 'Luis Patiño'), (18, 'Luis Sanipatin'), (19, 'Freddy Quinde'), (20, 'Felix Paguay'), (21, 'FRANKLIN ROSERO')], max_length=15, verbose_name='Primer Docente'),
        ),
        migrations.AlterField(
            model_name='tribunal',
            name='primerDocenteSuplente',
            field=models.CharField(choices=[(2, 'Georgina Arcos'), (3, 'Carlitos Guano'), (4, 'Katherin Siza'), (5, 'Jeffery Naranjo'), (6, 'Morillo Reynaldo'), (7, 'Marco Yandun'), (8, 'Genoveva Chulde'), (9, 'Kevin Lopez'), (10, 'Kelly Mora'), (11, 'Patricio Narvaez'), (12, 'Jorge Miranda'), (13, 'Samuel Lascano'), (14, 'Andy Mauricio Lopez'), (15, 'JENNIFER BERENICE BOLAÑOS GUERRON'), (16, 'Milton Del Hierro'), (17, 'Luis Patiño'), (18, 'Luis Sanipatin'), (19, 'Freddy Quinde'), (20, 'Felix Paguay'), (21, 'FRANKLIN ROSERO')], max_length=15, verbose_name='Primer Docente Suplente'),
        ),
        migrations.AlterField(
            model_name='tribunal',
            name='segundoDocente',
            field=models.CharField(choices=[(2, 'Georgina Arcos'), (3, 'Carlitos Guano'), (4, 'Katherin Siza'), (5, 'Jeffery Naranjo'), (6, 'Morillo Reynaldo'), (7, 'Marco Yandun'), (8, 'Genoveva Chulde'), (9, 'Kevin Lopez'), (10, 'Kelly Mora'), (11, 'Patricio Narvaez'), (12, 'Jorge Miranda'), (13, 'Samuel Lascano'), (14, 'Andy Mauricio Lopez'), (15, 'JENNIFER BERENICE BOLAÑOS GUERRON'), (16, 'Milton Del Hierro'), (17, 'Luis Patiño'), (18, 'Luis Sanipatin'), (19, 'Freddy Quinde'), (20, 'Felix Paguay'), (21, 'FRANKLIN ROSERO')], max_length=15, verbose_name='Segundo Docente'),
        ),
        migrations.AlterField(
            model_name='tribunal',
            name='segundoDocenteSuplente',
            field=models.CharField(choices=[(2, 'Georgina Arcos'), (3, 'Carlitos Guano'), (4, 'Katherin Siza'), (5, 'Jeffery Naranjo'), (6, 'Morillo Reynaldo'), (7, 'Marco Yandun'), (8, 'Genoveva Chulde'), (9, 'Kevin Lopez'), (10, 'Kelly Mora'), (11, 'Patricio Narvaez'), (12, 'Jorge Miranda'), (13, 'Samuel Lascano'), (14, 'Andy Mauricio Lopez'), (15, 'JENNIFER BERENICE BOLAÑOS GUERRON'), (16, 'Milton Del Hierro'), (17, 'Luis Patiño'), (18, 'Luis Sanipatin'), (19, 'Freddy Quinde'), (20, 'Felix Paguay'), (21, 'FRANKLIN ROSERO')], max_length=15, verbose_name='Segundo Docente Suplente'),
        ),
        migrations.AlterField(
            model_name='tribunal',
            name='terceroDocente',
            field=models.CharField(choices=[(2, 'Georgina Arcos'), (3, 'Carlitos Guano'), (4, 'Katherin Siza'), (5, 'Jeffery Naranjo'), (6, 'Morillo Reynaldo'), (7, 'Marco Yandun'), (8, 'Genoveva Chulde'), (9, 'Kevin Lopez'), (10, 'Kelly Mora'), (11, 'Patricio Narvaez'), (12, 'Jorge Miranda'), (13, 'Samuel Lascano'), (14, 'Andy Mauricio Lopez'), (15, 'JENNIFER BERENICE BOLAÑOS GUERRON'), (16, 'Milton Del Hierro'), (17, 'Luis Patiño'), (18, 'Luis Sanipatin'), (19, 'Freddy Quinde'), (20, 'Felix Paguay'), (21, 'FRANKLIN ROSERO')], max_length=15, verbose_name='Tercer Docente'),
        ),
        migrations.AlterField(
            model_name='tribunal',
            name='terceroDocenteSuplente',
            field=models.CharField(choices=[(2, 'Georgina Arcos'), (3, 'Carlitos Guano'), (4, 'Katherin Siza'), (5, 'Jeffery Naranjo'), (6, 'Morillo Reynaldo'), (7, 'Marco Yandun'), (8, 'Genoveva Chulde'), (9, 'Kevin Lopez'), (10, 'Kelly Mora'), (11, 'Patricio Narvaez'), (12, 'Jorge Miranda'), (13, 'Samuel Lascano'), (14, 'Andy Mauricio Lopez'), (15, 'JENNIFER BERENICE BOLAÑOS GUERRON'), (16, 'Milton Del Hierro'), (17, 'Luis Patiño'), (18, 'Luis Sanipatin'), (19, 'Freddy Quinde'), (20, 'Felix Paguay'), (21, 'FRANKLIN ROSERO')], max_length=15, verbose_name='Tercer Docente Suplente'),
        ),
        migrations.DeleteModel(
            name='Imagenes',
        ),
        migrations.DeleteModel(
            name='Informacion',
        ),
    ]
