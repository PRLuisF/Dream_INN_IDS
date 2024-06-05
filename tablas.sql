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
    nombre VARCHAR(100) NOT NULL,
    appellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    fecha_ingreso DATE NOT NULL,
    fecha_salida DATE NOT NULL,
    FOREIGN KEY (habitacion) REFERENCES habitaciones(habitacion)
);

INSERT INTO habitaciones VALUES (100,4,100000,"Una habitacion con cuatro camas individuales.","estandar");
INSERT INTO habitaciones VALUES (101,6,150000,"Una habitacion con una cama doble y otra habitacion con cuatro camas individuales .","estandar");
INSERT INTO habitaciones VALUES (102,2,70000,"Una habitacion con una cama doble.","estandar");
INSERT INTO habitaciones VALUES (103,5,100000,"Una habitacion con cinco camas individuales.","estandar");
INSERT INTO habitaciones VALUES (104,4,200000,"Una habitacion con una cama doble, un escritorio y otra habitacion con dos camas individuales.Ambas cuentan con television y vista al mar","deluxe");
INSERT INTO habitaciones VALUES (105,2,150000,"Una habitacion con una cama doble, un escritorio,una television y vista al mar.","deluxe");
INSERT INTO habitaciones VALUES (106,2,70000,"Una habitacion con una cama doble y dos camas individuales.","estandar");
INSERT INTO habitaciones VALUES (107,4,100000,"Una habitacion con dos camas individuales.","estandar");



