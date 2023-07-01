# Generated by Django 4.1.1 on 2023-06-17 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0013_alter_proyecto_iddocente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='idDocente',
            field=models.PositiveIntegerField(choices=[(17, 'MSc. Rita Amparo Caicedo Melo'), (18, 'MSc. Diego Armando Muñoz Tulcanaza'), (19, 'MSc. Hada Esther Solórzano Robinson'), (20, 'MSc. Veronica Del Pilar Coral Egas'), (21, 'MSc. Jairo Ricardo Chávez Rosero'), (22, 'MSc. Luis Arturo Vela Cepeda'), (23, 'MSc. Lorena Elizabeth Ruano Enriquez'), (24, 'MSc. Gustavo Armando Lucero Lima'), (25, 'MSc. Diana Paola Narvaez Tates'), (26, 'MSc. Gabriela Mercedes Mafla Medina'), (27, 'MSc. Omar Ricardo Oña Rocha'), (28, 'MSc. Jennifer Estefanía Pabón Ruíz'), (29, 'MSc. Edgar Fernando Pazmiño Palma'), (30, 'MSc. Juan Carlos Pilacuan España'), (31, 'MSc. Lucy Rosmeri Pillajo Perez'), (32, 'MSc. Marilin Morelia Polo Borga'), (33, 'MSc. Jorge Andrés Portilla Padilla'), (34, 'MSc. Aida Karina Pozo Burgos')], verbose_name='Docente Tutor del Proyecto'),
        ),
    ]
