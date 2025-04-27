DROP PROCEDURE AddOrUpdateItemCarrito;
CREATE DEFINER=`user_pr`@`localhost` PROCEDURE `AddOrUpdateItemCarrito`(
    IN p_carrito_id INT,
    IN p_producto_id INT,
    IN p_nombre VARCHAR(255),
    IN p_cantidad INT,
    IN p_precio DECIMAL(10,2)
)
BEGIN
    DECLARE cantidad_existente INT;
    DECLARE id_item INT;

    -- Verificamos si el producto ya está en el carrito
    SELECT cantidad INTO cantidad_existente
    FROM CarritoItem
    WHERE carrito_id = p_carrito_id AND producto_id = p_producto_id;

    IF cantidad_existente IS NOT NULL THEN
        -- Si el producto ya está en el carrito, actualizamos la cantidad
        UPDATE CarritoItem
        SET cantidad = cantidad_existente + 1
        WHERE carrito_id = p_carrito_id AND producto_id = p_producto_id;
    ELSE
        -- Si el producto no está en el carrito, lo insertamos
        INSERT INTO CarritoItem (carrito_id, producto_id, nombre, cantidad, precio)
        VALUES (p_carrito_id, p_producto_id, p_nombre, p_cantidad, p_precio);
    END IF;

    SELECT id INTO id_item FROM CarritoItem WHERE carrito_id = p_carrito_id AND producto_id = p_producto_id;
    
END

DROP PROCEDURE CreateUser;
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

    SELECT id INTO id_U FROM Usuario WHERE dni = p_dni;

    COMMIT;

    SELECT id_U AS id;
END