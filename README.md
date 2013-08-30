Monitores
=========

Aplicación de reserva de monitores en la _venta de monitores :tv: 2013_ del
lab :school:, también se usó como prueba de concepto para
_alembic_+_sqlalchemy_+_flask_ :triumph:.

Dependencias
------------

Se listan las versiones usadas para desarrollar, pero versiones un poco
antiguas (por ejemplo Flask 0.9) también deberían funcionar

* Flask
* Flasl-SQLAlchemy
* alembic
* python-ldap

Además, la biblioteca de la base de datos deseada para python (_psycopg2_ para
postgres y _pysqlite_ para sqlite), y flup para fastcgi.

Configuración
-------------

El programa espera un archivo llamado config.py en el directorio _instance_, o
indicado por la variable de entorno _MONITORES_SETTINGS_. Se incluye un ejemplo
en la carpeta examples :sweat:.

Creando tablas
--------------

Para crear las tablas en la base de datos **Despues de haber configurado
_SQLALCHEMY_DATABASE_URI_**, se debe ejecutar:

    alembic upgrade head

Este comando ejecutará todas las migraciones, creando las tablas necesarias.

