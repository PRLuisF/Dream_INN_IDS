# Dream_INN_IDS
Proyecto para la materia Introducción a desarrollo de software de FIUBA.

## Inicialización.
Para poder instalar las dependencias del proyecto, se debera tener instalado el gestor de entornos virtuales pipenv. Para comprobar si ya se tiene instalado, se puede ejecutar el comando:

```
pipenv --version
```

Si pipenv no esta instalado, se puede usar el siguiente comando para instalarlo:

```
sudo apt install pipenv
```

Una vez pipenv este instalado, se debe ejecutar el siguiente script en la misma carpeta donde se encuentra:

```
bash init.sh
```

Hecho esto, podrá empezar a trabajar en el proyecto.

## Cómo inicializar la Base de Datos
Requisitos previos: tener instalado Xampp (paquete de software libre que gestiona bases de datos MySQL, el servidor web Apache y los intérpretes para lenguajes PHP y Perl).
Para inicializar la base de datos, se debe importar el archivo tablas.sql en el servidor web de Xampp (url: 'localhost/phpmyadmin').
1. Hacer click en la pestaña Importar
2. En 'browse files', seleccionar el archivo tablas.sql
3. Hacer click en Import

Una vez hecho esto, se habrá creado la base de datos dreaminn_db, y desde Xampp se podrá acceder a las dos tablas que contiene (habitaciones y reservas).
Para modificar, agregar o quitar datos de la base, se deben utilizar los servicios de la API correspondientes, junto con
Postman.