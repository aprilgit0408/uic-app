# Generated by Django 4.1.1 on 2022-12-03 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_alter_nombrearchivolistaverificacion_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tutoria',
            old_name='fecha',
            new_name='fechaTutoria',
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='idDocente',
            field=models.PositiveIntegerField(choices=[(17, 'Rita Amparo Caicedo Melo'), (18, 'Diego Armando Muñoz Tulcanaza'), (19, 'Hada Esther Solórzano Robinson'), (20, 'Veronica Del Pilar Coral Egas'), (21, 'Jairo Ricardo Chávez Rosero'), (22, 'Luis Arturo Vela Cepeda'), (23, 'Lorena Elizabeth Ruano Enriquez'), (24, 'Gustavo Armando Lucero Lima'), (25, 'Diana Paola Narvaez Tates'), (26, 'Gabriela Mercedes Mafla Medina'), (27, 'Omar Ricardo Oña Rocha'), (28, 'Jennifer Estefanía Pabón Ruíz'), (29, 'Edgar Fernando Pazmiño Palma'), (30, 'Juan Carlos Pilacuan España'), (31, 'Lucy Rosmeri Pillajo Perez'), (32, 'Marilin Morelia Polo Borga'), (33, 'Jorge Andrés Portilla Padilla'), (34, 'Aida Karina Pozo Burgos')], verbose_name='Docente'),
        ),
        migrations.AlterField(
            model_name='tribunal',
            name='aula',
            field=models.CharField(choices=[('1', 'Aula 1'), ('2', 'Aula 2'), ('3', 'Aula 3'), ('4', 'Aula 4'), ('5', 'Aula 5'), ('6', 'Aula 6'), ('7', 'Aula 7'), ('8', 'Aula 8'), ('9', 'Aula 9')], max_length=20, verbose_name='Aula de defensa asignada'),
        ),
    ]
