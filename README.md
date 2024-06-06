# Dream_INN_IDS
Proyecto para la materia Introducción a desarrollo de software de FIUBA.

## Inicialización.
Para poder instalar las dependencias del proyecto, se debera tener instalado el gestor de paquetes de python pip. Para comprobar si ya se tiene instalado, se puede ejecutar el comando:

```
pip --version
```

Si pip no esta instalado, se debe ejecutar el siguiente comando, se deben seguir los pasos de la guia de instalacion de pip: https://pip.pypa.io/en/stable/installation/

- Se debe descargar el archivo get-pip.py
- Se debe ejecutar el archivo para instalar pip

Una vez asegurado que pip este en el sistema, se debe ejecutar el comando:

```
bash init.sh
```

Dentro de la carpeta donde esta ubicado init.sh, este script requiere que bash para ser ejecutado. Una vez hecho esto, se debe ejecutar el comando.

```
. .venv/bin/activate
```

Y podrá empezar a trabajar en el proyecto.

## Cómo inicializar la Base de Datos
Requisitos previos: tener instalado Xampp (paquete de software libre que gestiona bases de datos MySQL, el servidor web Apache y los intérpretes para lenguajes PHP y Perl).
Para inicializar la base de datos, se debe importar el archivo tablas.sql en el servidor web de Xampp (url: 'localhost/phpmyadmin').
1. Hacer click en la pestaña Importar
2. En 'browse files', seleccionar el archivo tablas.sql
3. Hacer click en Import

Una vez hecho esto, se habrá creado la base de datos dreaminn_db, y desde Xampp se podrá acceder a las tres tablas que contiene (Habitaciones_Particulares, Reserva_Especifica, Tipo_Habitaciones).
