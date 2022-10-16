
UIC APP
Instalar los archivos de la carpeta instaladores

1. ejecutar los requerimientos necesarios: pip install -r requirements.txt esto se ejecuta una sola vez
2. realizar los siguientes pasos en caso de que la base de datos esté llena, casi contrario ejecutar el paso 3
	0. Eliminar todos los cambios en el proyecto
	1. git pull
	2. Eliminar las migraciones de Usuarios/migratios y App/migrations excepto __init__
	3. Comentar la línea de 'App.apps.AppConfig' del archivo uicApp/settings.py linea 41
	4. comentar la línea de 22 de uicApp/url  # path('', include('App.urls')) esa es
	5. correr los comandos de:
		py .\manage.py makemigrations
		py .\manage.py migrate
	6. descomentar las líneas del paso 3 y 4, y correr el paso 5.
	7. py .\manage.py runserver
3. Creación del proyecto
	0. Eliminar todos los cambios en el proyecto
	1. git pull
	2. Eliminar las migraciones de Usuarios/migratios y App/migrations excepto __init__
	3. Comentar la línea de 'App.apps.AppConfig' del archivo uicApp/settings.py linea 41
	4. comentar la línea de 22 de uicApp/url  # path('', include('App.urls')) esa es
	5. correr los comandos de:
		py .\manage.py makemigrations
		py .\manage.py migrate
	6. creación de super usuario con el comando : py .\manage.py createsuperuser   - llenar todos los campos
	7. ejecutar script solo de constantes.
	8. descomentar las líneas del paso 3 y 4, y correr el paso 5.
	9. py .\manage.py runserver
