
-- Crear la tabla Usuario
CREATE TABLE Usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,  
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    contraseña_hash TEXT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear la tabla Producto
CREATE TABLE Producto (
    id INT AUTO_INCREMENT PRIMARY KEY,  
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    stock INTEGER NOT NULL,
    imagen_url TEXT
);

-- Crear la tabla Carrito
CREATE TABLE Carrito (
    id INT AUTO_INCREMENT PRIMARY KEY,  
    usuario_id INT, 
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id) ON DELETE CASCADE
);

-- Tabla CarritoItem
CREATE TABLE CarritoItem (
    id INT AUTO_INCREMENT PRIMARY KEY,
    carrito_id INT,  
    producto_id INT,  
    cantidad INTEGER NOT NULL,
    UNIQUE(carrito_id, producto_id),  -- Evita duplicados del mismo producto
    FOREIGN KEY (carrito_id) REFERENCES Carrito(id) ON DELETE CASCADE,  -- Clave foránea a Carrito
    FOREIGN KEY (producto_id) REFERENCES Producto(id)  -- Clave foránea a Producto
);

-- Tabla Pedido
CREATE TABLE Pedido (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    usuario_id INT,  -- Tipo INT para la clave foránea
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(30) DEFAULT 'pendiente',
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id)  -- Clave foránea a Usuario
);

-- Tabla PedidoItem
CREATE TABLE PedidoItem (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    pedido_id INT,  
    producto_id INT,  
    cantidad INTEGER NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES Pedido(id) ON DELETE CASCADE,  -- Clave foránea a Pedido
    FOREIGN KEY (producto_id) REFERENCES Producto(id)  -- Clave foránea a Producto
);
