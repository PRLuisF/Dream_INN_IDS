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

CREATE TABLE Tipo_Habitacion (
    tipo_habitacion VARCHAR(50) PRIMARY KEY NOT NULL,
    descripcion VARCHAR(300) NOT NULL,
    precio INT NOT NULL
);