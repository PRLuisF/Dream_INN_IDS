CREATE DATABASE dreaminn_db;
use dreaminn_db;

CREATE TABLE habitaciones (
    habitacion INT PRIMARY KEY NOT NULL,
    cantidad_personas INT NOT NULL,
    precio INT NOT NULL,
    descripcion VARCHAR(400) NOT NULL,
    categoria VARCHAR(100) NOT NULL
);

CREATE TABLE reservas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    habitacion INT NOT NULL,
    cantidad_personas INT NOT NULL,
    cantidad_noches INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    fecha_ingreso DATE NOT NULL,
    FOREIGN KEY (habitacion) REFERENCES habitaciones(habitacion)
);