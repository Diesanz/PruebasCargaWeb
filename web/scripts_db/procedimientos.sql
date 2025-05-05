-- Active: 1744363405273@@127.0.0.1@3306@Carga_web
-- Primero eliminamos el procedimiento si ya existe
DROP PROCEDURE AddOrUpdateItemCarrito;

-- Crear el procedimiento para agregar o actualizar un ítem en el carrito
CREATE DEFINER=`user_pr`@`localhost` PROCEDURE `AddOrUpdateItemCarrito`(
    IN p_carrito_id INT,          -- ID del carrito
    IN p_producto_id INT,         -- ID del producto
    IN p_nombre VARCHAR(255),     -- Nombre del producto
    IN p_cantidad INT,            -- Cantidad del producto
    IN p_precio DECIMAL(10,2)     -- Precio del producto
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
        INSERT INTO CarritoItem (carrito_id, producto_id, nombre, cantidad, precio)
        VALUES (p_carrito_id, p_producto_id, p_nombre, p_cantidad, p_precio);  -- Insertamos los datos proporcionados
    END IF;
END;

-- Primero eliminamos el procedimiento si ya existe
DROP PROCEDURE CreateUser;

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