CREATE DATABASE dreaminn_db;
use dreaminn_db;

CREATE TABLE reservas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    habitacion INT,
    nombre VARCHAR(100) NOT NULL,
    appellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    fecha_ingreso DATE NOT NULL,
    fecha_salida DATE NOT NULL,
    FOREIGN KEY (habitacion) REFERENCES habitaciones(habitacion)
);

CREATE TABLE habitaciones (
    habitacion INT PRIMARY KEY NOT NULL,
    cantidad_personas INT NOT NULL,
    precio INT NOT NULL,
    descripcion VARCHAR(400) NOT NULL,
    categoria VARCHAR(100) NOT NULL
);


