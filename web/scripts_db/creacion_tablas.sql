-- Active: 1744363405273@@127.0.0.1@3306@Carga_web

-- CREATE DATABASE Carga_web;
-- CREATE USER 'user_pr'@'localhost' IDENTIFIED BY 'Grupo6esi';
-- GRANT ALL PRIVILEGES ON Carga_web.* TO 'user_pr'@'localhost';
-- FLUSH PRIVILEGES;

DROP TABLE IF EXISTS `PedidoItem`;
DROP TABLE IF EXISTS `Pedido`;
DROP TABLE IF EXISTS `CarritoItem`;
DROP TABLE IF EXISTS `Carrito`;
DROP TABLE IF EXISTS `Producto`;
DROP TABLE IF EXISTS `Usuario`;

-- Crear la tabla Usuario
CREATE TABLE `Usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `dni` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `domicilio` varchar(255) NOT NULL,
  `fechaCreacion` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `password` text NOT NULL,
  PRIMARY KEY (`id`)
);

-- Crear la tabla Producto
CREATE TABLE `Producto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL,
  `stock` int NOT NULL,
  `tipo` varchar(100) NOT NULL,
  `imagen_url` text DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- Crear la tabla Carrito
CREATE TABLE `Carrito` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `Carrito_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `Usuario` (`id`) ON DELETE CASCADE
);

-- Crear la tabla CarritoItem
CREATE TABLE `CarritoItem` (
  `id` int NOT NULL AUTO_INCREMENT,
  `carrito_id` int DEFAULT NULL,
  `producto_id` int DEFAULT NULL,
  `nombre` varchar(255) NOT NULL,
  `cantidad` int NOT NULL,
  `precio` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `carrito_id` (`carrito_id`,`producto_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `CarritoItem_ibfk_1` FOREIGN KEY (`carrito_id`) REFERENCES `Carrito` (`id`) ON DELETE CASCADE,
  CONSTRAINT `CarritoItem_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `Producto` (`id`)
);

-- Crear la tabla Pedido
CREATE TABLE `Pedido` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `fecha` timestamp NULL DEFAULT current_timestamp(),
  `estado` varchar(30) DEFAULT 'pendiente',
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `Pedido_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `Usuario` (`id`)
);

-- Crear la tabla PedidoItem
CREATE TABLE `PedidoItem` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedido_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pedido_id` (`pedido_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `PedidoItem_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `Pedido` (`id`) ON DELETE CASCADE,
  CONSTRAINT `PedidoItem_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `Producto` (`id`)
);
