CREATE TABLE Reserva_Especifica (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    tipo_habitacion VARCHAR(50) NOT NULL,
    numero_habitacion INT NOT NULL,
    fecha_entrada DATE NOT NULL,
    fecha_salida DATE NOT NULL
);

CREATE TABLE Habitaciones_Particulares (
    numero_habitacion INT PRIMARY KEY NOT NULL,
    tipo_habitacion VARCHAR(50) NOT NULL,
    estado BOOLEAN NOT NULL
);

CREATE TABLE Tipo_Habitaciones (
    tipo_habitacion VARCHAR(50) PRIMARY KEY NOT NULL,
    descripcion VARCHAR(300) NOT NULL,
    precio INT NOT NULL
);

INSERT INTO Tipo_Habitaciones VALUES ('Simple','Tiene una cama, una television,un escritorio y un frigobar',40000);
INSERT INTO Tipo_Habitaciones VALUES ('Doble','Tiene dos camas, una television,un escritorio y un frigobar',70000);
INSERT INTO Tipo_Habitaciones VALUES ('Familiar','Tiene cuatro camas, una television,dos escritorio y un frigobar',100000);

