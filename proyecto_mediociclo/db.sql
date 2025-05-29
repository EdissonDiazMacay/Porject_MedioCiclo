CREATE DATABASE IF NOT EXISTS py_programacionavanzada;
use py_programacionavanzada;

DROP TABLE IF EXISTS cliente;
CREATE TABLE `cliente`(
    id INT PRIMARY KEY AUTO_INCREMENT,
    cedula CHAR(10) NOT NULL,
    nombres VARCHAR(30) NOT NULL,
    apellidos VARCHAR(30) NOT NULL
)Engine=InnoDB AUTO_INCREMENT = 1;

DROP TABLE IF EXISTS deuda;
CREATE TABLE `deuda`(
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT NOT NULL,
    monto FLOAT NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id)
)Engine=InnoDB AUTO_INCREMENT = 1;

DROP TABLE IF EXISTS pago;
CREATE TABLE `pago`(
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT NOT NULL,
    monto FLOAT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id)
)Engine=InnoDB AUTO_INCREMENT = 1;
