# Generated by Django 4.1.1 on 2023-04-23 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0003_remove_documento_idperfiles_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='documento',
            name='nombre',
            field=models.CharField(max_length=200, verbose_name='Nombre del Documento'),
        ),
    ]