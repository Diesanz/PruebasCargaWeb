
-- Active: 1745919767174@@127.0.0.1@3306@carga_web
/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.8.1-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: Carga_web
-- ------------------------------------------------------
-- Server version	11.8.1-MariaDB-2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `Usuario`
--

DROP TABLE IF EXISTS `Usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `dni` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `domicilio` varchar(255) NOT NULL,
  `fechaCreacion` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `password` text NOT NULL,
  PRIMARY KEY (`id`)
)  ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Usuario`
--

LOCK TABLES `Usuario` WRITE;
/*!40000 ALTER TABLE `Usuario` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `Usuario` VALUES
(8,'Diego','719Q','d@d','Palencia','2025-04-12 16:11:26','123'),
(31,'Pepe','12312D','pep@pepito.com','Luna','2025-04-13 14:02:42','1231'),
(34,'Juan','12341222','eatthiscr@gmail.com','Paja','2025-04-17 15:06:27','123'),
(35,'Lima','908090Q','l@l.com','caca','2025-04-25 17:52:27','1'),
(36,'lolas','908757w','lola@l.com','lopa','2025-04-25 17:56:53','1'),
(37,'k','67806q','k@k.com','k','2025-04-25 17:59:34','1'),
(38,'lo','6879579','lo@lo.com','hu','2025-04-25 18:00:56','1'),
(39,'DiegoSanz','7198859Q','d@3d.com','Palencia','2025-04-25 22:10:32','1234');
/*!40000 ALTER TABLE `Usuario` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `Producto`
--

DROP TABLE IF EXISTS `Producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Producto` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL,
  `stock` int(11) NOT NULL,
  `tipo` varchar(100) NOT NULL,
  `imagen_url` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Producto`
--

LOCK TABLES `Producto` WRITE;
/*!40000 ALTER TABLE `Producto` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `Producto` VALUES
(1,'Ensalada de Pavo y Pina','1 lechuga. 200 gramos de pechuga de pavo asada. 200 gramos de queso feta. 90 gramos de cebollitas encurtidas. 1 lata de maíz dulce. 6 rodajas de piña, con su jugo. 1 zanahoria',10.50,1,'Equilibrado','ensaladaPavoPina.jpg'),
(2,'Pasta carbonara','400 g de spaghetti Garofalo. 200 g de panceta curada de cerdo. 50 g de queso Parmigiano Reggiano. 3 yemas y 1 huevo entero',9.80,80,'Equilibrado','pastacarbonara.jpg'),
(3,'Guisantes con Jamon y Sepia','3 dientes de ajo. 50 g de aceite de oliva. 300 g de sepia limpia. 90 - 100 g de jamón curado en dados. 100 g de vino blanco. 500 g de guisantes congelados',11.20,60,'Equilibrado','guisantesconjamonysepia.jpg'),
(4,'Calabacines rellenos','4 calabacines medianos. 2 cebollas. 1 diente de ajo. 300 ml de bechamel. 100 g de queso rallado para gratinar',8.90,90,'Equilibrado','calabacinesrellenos.jpg'),
(5,'Arroz tres delicias','400 g de arroz. 1 zanahoria. 75 g de gambas. 75 g de guisantes. 75 g de jamon york. 20 ml de salsa de soja. 2 huevos.',9.30,70,'Equilibrado','arroztresdelicias.jpg'),
(6,'Potaje de Garbanzos con Espinacas','200g de garbanzos frescos. 2 cebolletas. 1 hoja de laurel. 1 manojo de espinaca fresca. Sal y aceite de oliva virgen extra.',8.70,75,'Vegano','potajedegarbanzosconespinacas.jpg'),
(7,'Ratatouille','350 g de Tomate frito. 300 g de calabacín. 550 g de berenjena. 600 g de tomate. 200 g de cebolla. 5 dientes de ajo. Orégano al gusto. Sal y dos cucharadas de aceite de oliva',9.50,90,'Vegano','ratatouille.jpg'),
(8,'Arroz con Verduras','4 dientes de ajo. 1 tomate. 100 gramos de arroz integral. 1 cucharadita de pimenton dulce. Agua y aceite de oliva virgen extra.',7.90,100,'Vegano','arrozconverduras.jpg'),
(9,'Tortilla vegana de Calabacin','60 g de harina de garbanzos. 1 calabacín grande. 1/4 cucharadita de sal. 1 cucharadita de cúrcuma molida. 120 ml de agua. Aceite de oliva virgen extra.',6.50,110,'Vegano','tortillaveganadecalabacin.jpg'),
(10,'Alubias con almejas','400 g de alubia blanca redonda. 400 g de almejas. Media cebolla. 4 dientes de ajo. Un trozo de pimiento rojo y otro verde. Una hoja de laurel. Un puerro. Sal, pimienta y perejil picado',12.50,70,'Proteico','alubiasconalmejas.jpg'),
(11,'Garbanzos con Espinacas y Bacalao','200 g de garbanzos frescos. 200 g de bacalao. 500 ml de caldo de pescado. 150 g de espinaca fresca o congelada. 1 huevo cocido. 2 dientes de ajo.',11.30,90,'Proteico','garbanzosespinacasbacalao.jpg'),
(12,'Lentejas con Pollo y Manzana','200 g de lentejas. 250 g de pechuga de pollo. 150 g de manzana. 100g de cebolla. Agua y aceite de oliva virgen extra',10.90,60,'Proteico','lentejaspollomanzana.jpg'),
(13,'Estofado de Ternera','500g de ternera. 1 cebolla. 1 zanahoria. 1 diente de ajo. 250 g de caldo de carne. Sal y pimienta al gusto.',13.00,55,'Proteico','estofadodeternera.jpg');

/*!40000 ALTER TABLE `Producto` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `Carrito`
--

DROP TABLE IF EXISTS `Carrito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Carrito` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `Carrito_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `Usuario` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Carrito`
--

LOCK TABLES `Carrito` WRITE;
/*!40000 ALTER TABLE `Carrito` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `Carrito` VALUES
(1,31),
(2,34),
(3,35),
(4,36),
(5,37),
(6,38),
(7,39);
/*!40000 ALTER TABLE `Carrito` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `CarritoItem`
--

DROP TABLE IF EXISTS `CarritoItem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `CarritoItem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `carrito_id` int(11) DEFAULT NULL,
  `producto_id` int(11) DEFAULT NULL,
  `nombre` varchar(255) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `carrito_id` (`carrito_id`,`producto_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `CarritoItem_ibfk_1` FOREIGN KEY (`carrito_id`) REFERENCES `Carrito` (`id`) ON DELETE CASCADE,
  CONSTRAINT `CarritoItem_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `Producto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CarritoItem`
--

LOCK TABLES `CarritoItem` WRITE;
/*!40000 ALTER TABLE `CarritoItem` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `CarritoItem` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `Pedido`
--

DROP TABLE IF EXISTS `Pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Pedido` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) DEFAULT NULL,
  `fecha` timestamp NULL DEFAULT current_timestamp(),
  `estado` varchar(30) DEFAULT 'pendiente',
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `Pedido_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `Usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=87 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pedido`
--

LOCK TABLES `Pedido` WRITE;
/*!40000 ALTER TABLE `Pedido` DISABLE KEYS */;
set autocommit=0;

/*!40000 ALTER TABLE `Pedido` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `PedidoItem`
--

DROP TABLE IF EXISTS `PedidoItem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `PedidoItem` (
  `id` int(110) NOT NULL AUTO_INCREMENT,
  `pedido_id` int(110) NOT NULL,
  `producto_id` int(110) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pedido_id` (`pedido_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `PedidoItem_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `Pedido` (`id`) ON DELETE CASCADE,
  CONSTRAINT `PedidoItem_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `Producto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=117 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PedidoItem`
--

LOCK TABLES `PedidoItem` WRITE;
/*!40000 ALTER TABLE `PedidoItem` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `PedidoItem` VALUES
(97,78,2,11,12),
(98,78,3,11,12),
(101,79,2,11,12),
(102,79,3,11,12),
(103,80,2,11,12),
(104,80,3,11,12),
(113,82,2,11,1),
(114,82,2,11,1),
(115,85,2,1,2),
(116,86,3,1,2);
/*!40000 ALTER TABLE `PedidoItem` ENABLE KEYS */;
UNLOCK TABLES;
commit;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-04-28  1:19:53
/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.8.1-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: Carga_web
-- ------------------------------------------------------
-- Server version	11.8.1-MariaDB-2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Dumping data for table `CarritoItem`
--

LOCK TABLES `CarritoItem` WRITE;
/*!40000 ALTER TABLE `CarritoItem` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `CarritoItem` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `Pedido`
--

LOCK TABLES `Pedido` WRITE;
/*!40000 ALTER TABLE `Pedido` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `Pedido` VALUES
(30,39,'2025-04-27 22:04:23','Pendiente'),
(31,39,'2025-04-27 22:04:24','Pendiente'),
(32,39,'2025-04-27 22:07:38','Pendiente'),
(33,39,'2025-04-27 22:07:39','Pendiente'),
(34,39,'2025-04-27 22:07:40','Pendiente'),
(35,39,'2025-04-27 22:07:41','Pendiente'),
(36,39,'2025-04-27 22:07:51','Pendiente'),
(37,39,'2025-04-27 22:08:41','Pendiente'),
(38,39,'2025-04-27 22:08:42','Pendiente'),
(39,39,'2025-04-27 22:09:14','Pendiente'),
(40,39,'2025-04-27 22:09:15','Pendiente'),
(41,39,'2025-04-27 22:10:24','Pendiente'),
(42,39,'2025-04-27 22:10:24','Pendiente'),
(43,39,'2025-04-27 22:10:25','Pendiente'),
(44,39,'2025-04-27 22:10:25','Pendiente'),
(45,39,'2025-04-27 22:12:12','Pendiente'),
(46,39,'2025-04-27 22:12:14','Pendiente'),
(47,39,'2025-04-27 22:13:22','Pendiente'),
(48,39,'2025-04-27 22:13:23','Pendiente'),
(49,39,'2025-04-27 22:15:11','Pendiente'),
(50,39,'2025-04-27 22:17:57','Pendiente'),
(51,39,'2025-04-27 22:19:18','Pendiente'),
(52,39,'2025-04-27 22:20:13','Pendiente'),
(53,39,'2025-04-27 22:21:26','Pendiente'),
(54,39,'2025-04-27 22:21:29','Pendiente'),
(55,39,'2025-04-27 22:21:30','Pendiente'),
(56,39,'2025-04-27 22:23:13','Pendiente'),
(57,39,'2025-04-27 22:23:48','Pendiente'),
(58,39,'2025-04-27 22:24:11','Pendiente'),
(59,39,'2025-04-27 22:25:44','Pendiente'),
(60,39,'2025-04-27 22:25:45','Pendiente'),
(61,39,'2025-04-27 22:26:27','Pendiente'),
(62,39,'2025-04-27 22:30:27','Pendiente'),
(63,39,'2025-04-27 22:31:21','Pendiente'),
(64,39,'2025-04-27 22:31:40','Pendiente'),
(65,39,'2025-04-27 22:31:53','Pendiente'),
(66,39,'2025-04-27 22:32:22','Pendiente'),
(67,39,'2025-04-27 22:32:30','Pendiente'),
(68,39,'2025-04-27 22:33:21','Pendiente'),
(69,39,'2025-04-27 22:33:40','Pendiente'),
(70,39,'2025-04-27 22:33:43','Pendiente'),
(71,39,'2025-04-27 22:34:48','Pendiente'),
(72,39,'2025-04-27 22:34:54','Pendiente'),
(73,39,'2025-04-27 22:40:19','Pendiente'),
(74,39,'2025-04-27 22:40:25','Pendiente'),
(75,39,'2025-04-27 22:42:02','Pendiente'),
(76,39,'2025-04-27 22:43:09','Pendiente'),
(77,39,'2025-04-27 22:43:16','Pendiente'),
(78,39,'2025-04-27 22:43:30','Pendiente'),
(79,39,'2025-04-27 22:43:58','Pendiente'),
(80,39,'2025-04-27 22:51:12','Pendiente'),
(81,39,'2025-04-27 22:53:12','Pendiente'),
(82,39,'2025-04-27 22:53:24','Pendiente'),
(83,39,'2025-04-27 23:00:32','Pendiente'),
(84,39,'2025-04-27 23:00:33','Pendiente'),
(85,39,'2025-04-27 23:13:52','Pendiente'),
(86,39,'2025-04-27 23:17:46','Pendiente');
/*!40000 ALTER TABLE `Pedido` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping routines for database 'Carga_web'
--
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AddOrUpdateItemCarrito` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
DELIMITER ;;
CREATE DEFINER=`user_pr`@`localhost` PROCEDURE `AddOrUpdateItemCarrito`(
    IN p_carrito_id INT,
    IN p_producto_id INT,
    IN p_nombre VARCHAR(255),
    IN p_cantidad INT,
    IN p_precio DECIMAL(10,2)
)
BEGIN
    DECLARE cantidad_existente INT;

    -- Verificamos si el producto ya está en el carrito
    SELECT cantidad INTO cantidad_existente
    FROM CarritoItem
    WHERE carrito_id = p_carrito_id AND producto_id = p_producto_id;

    IF cantidad_existente IS NOT NULL THEN
        -- Si el producto ya está en el carrito, actualizamos la cantidad
        UPDATE CarritoItem
        SET cantidad = cantidad + 1
        WHERE carrito_id = p_carrito_id AND producto_id = p_producto_id;
    ELSE
        -- Si el producto no está en el carrito, lo insertamos
        INSERT INTO CarritoItem (carrito_id, producto_id, nombre, cantidad, precio)
        VALUES (p_carrito_id, p_producto_id, p_nombre, p_cantidad, p_precio);
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 DROP PROCEDURE IF EXISTS `CreateUser` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
DELIMITER ;;

CREATE DEFINER=`user_pr`@`localhost` PROCEDURE `CreateUser`(
    IN p_nombre VARCHAR(100),
    IN p_dni VARCHAR(20),
    IN p_email VARCHAR(100),
    IN p_domicilio VARCHAR(150),
    IN p_password VARCHAR(100)
)
BEGIN
    DECLARE id_U INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Ocurrió un error durante la transacción.';
    END;
    START TRANSACTION;
    INSERT INTO Usuario (nombre, dni, email, domicilio, password)
    VALUES (p_nombre, p_dni, p_email, p_domicilio, p_password);
    SET id_U = LAST_INSERT_ID();  -- Obtener directamente el último id insertado

    COMMIT;
    SELECT id_U AS id;
END;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-04-28  1:20:44

