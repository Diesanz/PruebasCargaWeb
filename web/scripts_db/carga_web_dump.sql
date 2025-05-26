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
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
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
  UNIQUE KEY `id` (`id`,`usuario_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `Carrito_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `Usuario` (`id`) ON DELETE CASCADE
);

-- Crear la tabla CarritoItem
CREATE TABLE `CarritoItem` (
  `id` int NOT NULL AUTO_INCREMENT,
  `carrito_id` int DEFAULT NULL,
  `producto_id` int DEFAULT NULL,
  `cantidad` int NOT NULL,
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
  `total` decimal(10,2), 
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
  `precio` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pedido_id` (`pedido_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `PedidoItem_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `Pedido` (`id`) ON DELETE CASCADE,
  CONSTRAINT `PedidoItem_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `Producto` (`id`)
);

-- Active: 1744363405273@@127.0.0.1@3306@Carga_web
-- Primero eliminamos el procedimiento si ya existe
DROP PROCEDURE IF EXISTS AddOrUpdateItemCarrito;

-- Crear el procedimiento para agregar o actualizar un ítem en el carrito
CREATE DEFINER=`user_pr`@`localhost` PROCEDURE `AddOrUpdateItemCarrito`(
    IN p_carrito_id INT,          -- ID del carrito
    IN p_producto_id INT,         -- ID del producto
    IN p_cantidad INT            -- Cantidad del producto
)
BEGIN
    DECLARE cantidad_existente INT;  -- Variable para almacenar la cantidad existente del producto en el carrito

    -- Verificamos si el producto ya está en el carrito
    SELECT cantidad INTO cantidad_existente
    FROM CarritoItem
    WHERE carrito_id = p_carrito_id AND producto_id = p_producto_id;

    -- Si el producto ya existe en el carrito, actualizamos la cantidad
    IF cantidad_existente IS NOT NULL THEN
        UPDATE CarritoItem
        SET cantidad = cantidad + p_cantidad  -- Sumamos la cantidad existente con la nueva cantidad
        WHERE carrito_id = p_carrito_id AND producto_id = p_producto_id;
    ELSE
        -- Si el producto no está en el carrito, lo insertamos como nuevo ítem
        INSERT INTO CarritoItem (carrito_id, producto_id, cantidad)
        VALUES (p_carrito_id, p_producto_id, p_cantidad);  -- Insertamos los datos proporcionados
    END IF;
END;

-- Primero eliminamos el procedimiento si ya existe
DROP PROCEDURE IF EXISTS CreateUser;

-- Crear el procedimiento para crear un nuevo usuario
CREATE DEFINER=`user_pr`@`localhost` PROCEDURE `CreateUser`(
    IN p_nombre VARCHAR(100),       -- Nombre del usuario
    IN p_dni VARCHAR(20),           -- DNI del usuario
    IN p_email VARCHAR(100),        -- Email del usuario
    IN p_domicilio VARCHAR(150),    -- Domicilio del usuario
    IN p_password VARCHAR(100)      -- Contraseña del usuario
)
BEGIN
    DECLARE id_U INT;  -- Variable para almacenar el ID del nuevo usuario
    DECLARE EXIT HANDLER FOR SQLEXCEPTION  -- Manejador de excepciones para capturar errores
    BEGIN
        ROLLBACK;  -- Si ocurre un error, deshacemos la transacción
        SIGNAL SQLSTATE '45000'  -- Lanza una señal con el mensaje de error
        SET MESSAGE_TEXT = 'Ocurrió un error durante la transacción.';  -- Mensaje de error personalizado
    END;
    
    -- Iniciamos la transacción
    START TRANSACTION;
    
    -- Insertamos el nuevo usuario en la tabla Usuario
    INSERT INTO Usuario (nombre, dni, email, domicilio, password)
    VALUES (p_nombre, p_dni, p_email, p_domicilio, p_password);

    -- Obtenemos el ID del nuevo usuario insertado
    SET id_U = LAST_INSERT_ID();  -- Recupera el último ID insertado (el del nuevo usuario)

    INSERT INTO Carrito (usuario_id) VALUES (id_U);

    -- Confirmamos la transacción
    COMMIT;
    
    -- Devolvemos el ID del nuevo usuario
    SELECT id_U AS id;
END;

INSERT INTO Producto (id,nombre, descripcion, precio, stock, tipo, imagen_url) VALUES
(1,'Ensalada de Pavo y Pina','1 lechuga. 200 gramos de pechuga de pavo asada. 200 gramos de queso feta. 90 gramos de cebollitas encurtidas. 1 lata de maíz dulce. 6 rodajas de piña, con su jugo. 1 zanahoria',10.50,1,'Equilibrado','ensaladadePavoyPina.jpg'),
(2,'Pasta carbonara','400 g de spaghetti Garofalo. 200 g de panceta curada de cerdo. 50 g de queso Parmigiano Reggiano. 3 yemas y 1 huevo entero',9.80,80,'Equilibrado','pastacarbonara.jpg'),
(3,'Guisantes con Jamon y Sepia','3 dientes de ajo. 50 g de aceite de oliva. 300 g de sepia limpia. 90 - 100 g de jamón curado en dados. 100 g de vino blanco. 500 g de guisantes congelados',11.20,60,'Equilibrado','guisantesconjamonysepia.jpg'),
(4,'Calabacines rellenos','4 calabacines medianos. 2 cebollas. 1 diente de ajo. 300 ml de bechamel. 100 g de queso rallado para gratinar',8.90,90,'Equilibrado','calabacinesrellenos.jpg'),
(5,'Arroz tres delicias','400 g de arroz. 1 zanahoria. 75 g de gambas. 75 g de guisantes. 75 g de jamon york. 20 ml de salsa de soja. 2 huevos.',9.30,70,'Equilibrado','arroztresdelicias.jpg'),
(6,'Potaje de Garbanzos con Espinacas','200g de garbanzos frescos. 2 cebolletas. 1 hoja de laurel. 1 manojo de espinaca fresca. Sal y aceite de oliva virgen extra.',8.70,75,'Vegano','potajedegarbanzosconespinacas.jpg'),
(7,'Ratatouille','350 g de Tomate frito. 300 g de calabacín. 550 g de berenjena. 600 g de tomate. 200 g de cebolla. 5 dientes de ajo. Orégano al gusto. Sal y dos cucharadas de aceite de oliva',9.50,90,'Vegano','ratatouille.jpg'),
(8,'Arroz con Verduras','4 dientes de ajo. 1 tomate. 100 gramos de arroz integral. 1 cucharadita de pimenton dulce. Agua y aceite de oliva virgen extra.',7.90,100,'Vegano','arrozconverduras.jpg'),
(9,'Tortilla vegana de Calabacin','60 g de harina de garbanzos. 1 calabacín grande. 1/4 cucharadita de sal. 1 cucharadita de cúrcuma molida. 120 ml de agua. Aceite de oliva virgen extra.',6.50,110,'Vegano','tortillaveganadecalabacin.jpg'),
(10,'Alubias con almejas','400 g de alubia blanca redonda. 400 g de almejas. Media cebolla. 4 dientes de ajo. Un trozo de pimiento rojo y otro verde. Una hoja de laurel. Un puerro. Sal, pimienta y perejil picado',12.50,70,'Proteico','alubiasconalmejas.jpg'),
(11,'Garbanzos con Espinacas y Bacalao','200 g de garbanzos frescos. 200 g de bacalao. 500 ml de caldo de pescado. 150 g de espinaca fresca o congelada. 1 huevo cocido. 2 dientes de ajo.',11.30,90,'Proteico','garbanzosconespinacasybacalao.jpg'),
(12,'Lentejas con Pollo y Manzana','200 g de lentejas. 250 g de pechuga de pollo. 150 g de manzana. 100g de cebolla. Agua y aceite de oliva virgen extra',10.90,60,'Proteico','lentejasconpolloymanzana.jpg'),
(13,'Estofado de Ternera','500g de ternera. 1 cebolla. 1 zanahoria. 1 diente de ajo. 250 g de caldo de carne. Sal y pimienta al gusto.',13.00,55,'Proteico','estofadodeternera.jpg');