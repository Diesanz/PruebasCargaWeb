function abrirModalEditar(id, nombre, descripcion, precio, stock, tipo) {
    document.getElementById('edit_id').value = id;
    document.getElementById('edit_nombre').value = nombre;
    document.getElementById('edit_descripcion').value = descripcion;
    document.getElementById('edit_precio').value = precio;
    document.getElementById('edit_stock').value = stock;
    document.getElementById('edit_tipo').value = tipo;

    document.getElementById('modalEditar').style.display = 'block';
}
function cerrarModal() {
    document.getElementById('modalEditar').style.display = 'none';
}

function actualizarProducto() {
    const id = document.getElementById('edit_id').value;

    const datos = {
        nombre: document.getElementById('edit_nombre').value,
        descripcion: document.getElementById('edit_descripcion').value,
        precio: document.getElementById('edit_precio').value,
        stock: document.getElementById('edit_stock').value,
        tipo: document.getElementById('edit_tipo').value
    };

    fetch(`/api/productos/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams(datos)
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect_url) {
            window.location.href = data.redirect_url;
        } else if (data.error) {
            alert("Error: " + data.error);
        }
    })
    .catch(error => {
        console.error("Error en la actualización:", error);
    });
}

function mostrarSelectTipo() {
    // Ocultar el texto del tipo y mostrar el select
    
    document.getElementById('nuevo_tipo').style.display = 'block';
    // También ocultamos el icono para no tenerlo visible mientras estamos seleccionando
    document.getElementById('editar-tipo').style.display = 'none';
}

function cambiarTipo() {
    var tipoSeleccionado = document.getElementById('nuevo_tipo').value;
    // Actualizar el texto del span con el valor seleccionado
    document.getElementById('tipo-plato').innerText = tipoSeleccionado;
    // Volver a mostrar el span y ocultar el select
    document.getElementById('nuevo_tipo').style.display = 'none';
    document.getElementById('tipo-plato').style.display = 'inline';
    // Volver a mostrar el icono
    document.getElementById('editar-tipo').style.display = 'inline';
    
    // Llamar a la función para actualizar el tipo de plato en el backend
    actualizarTipo(tipoSeleccionado);
}

function actualizarTipo(tipo) {
    const id = document.getElementById('tipo-plato').dataset.id;

    const datos = {
        tipo: tipo
    };

    fetch(`/api/productos/${id}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(datos)
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect_url) {
            window.location.href = data.redirect_url;
        } else if (data.error) {
            alert("Error: " + data.error);
        }
    })
    .catch(error => {
        console.error("Error al actualizar el tipo de plato:", error);
    });
}

function getCarrito() {
    // Redirige directamente a la ruta del carrito
    // El navegador se encargará de enviar automáticamente las cookies con el token
    window.location.href = '/api/carrito';
}

function insert_carrito(boton){
    
    boton.addEventListener("click", function () {
        const productoId = this.id;

        fetch("/api/carrito/agregar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id_producto: productoId,
                cantidad: 1  // puedes cambiarlo si necesitas permitir cantidades variables
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.redirect_url) {
                window.location.href = data.redirect_url;
            } else if (data.error) {
                alert("Inicia sesión antes de añadir productso");
            }
        })
        .catch(error => {
            alert("Hubo un error: " + error.message);
        });
    });
}

function borrar_items_carrito(){
    fetch('/api/carrito/vaciar', {
        method: 'DELETE',
      })
      .then(response => response.json())
      .then(data => {
        console.log('Productos eliminados:', data);
        getCarrito()
        // Aquí podrías actualizar la UI o mostrar un mensaje de éxito
      })
      .catch(error => {
        console.error('Error:', error);
    });
}

function tramitar_pedido(btn) {
    fetch('/api/checkout', {
        method: 'POST',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Respuesta no OK del servidor");
        }
        return response.json();
    })
    .then(data => {
        if (data.redirect_url) {
            // Redirigir si el backend lo indica
            window.location.href = data.redirect_url;
        } else if (data.id_pedido) {
            console.log('✅ Pedido realizado:', data);
            getCarrito()
        } else {
            console.warn("⚠️ Respuesta desconocida del servidor:", data);
        }
    })
    .catch(error => {
        console.error("❌ Error al tramitar pedido:", error);
    });
}


function hacerRegistro(registro){

    registro.addEventListener('submit', async(e) => {
        
        e.preventDefault();

        const datos = {
            nombre: document.getElementById('nombre').value,
            dni: document.getElementById('dni').value,
            email: document.getElementById('email').value,
            domicilio: document.getElementById('domicilio').value,
            password: document.getElementById('password').value
        };

        fetch(`/api/registro`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams(datos)
        })
        .then(response => response.json())
        .then(data => {
            if (data.redirect_url) {
                window.location.href = data.redirect_url;
            } else if (data.error) {
                alert("Error: " + data.error);
            }
        })
        .catch(error => {
            console.error("Error en el registro:", error);
        });
    });
}

async function hacerLogin(login){
    login.addEventListener('submit', async(e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    'email': email,
                    'password': password
                })
            });

            if (!response.ok) {
                throw new Error('Credenciales incorrectas o error desconocido');
            }

            // El token ya está en la cookie, el navegador lo enviará automáticamente
            const data = await response.json();
            window.location.href = '/'
            
        } catch (error) {
            // Mostrar el error en la página sin recargar
            const errorDiv = document.getElementById('mensaje-error');
            errorDiv.textContent = error.message;
            errorDiv.style.display = 'block';
        }
    });
}


// Espera a que todo el contenido del DOM esté cargado antes de ejecutar el script
document.addEventListener('DOMContentLoaded', function(){
    // Referencias a elementos del DOM
    const login = document.getElementById('loginForm');
    const registro = document.getElementById('formRegistro');
    const carrito = document.getElementById('carrito');
    const delete_btn = document.getElementById('delete_btn');
    const logout_btn = document.getElementById('logoutButton');
    const tramitar_btn = document.getElementById('tramitar_btn');
    const insert_pr_btn = document.querySelectorAll(".boton1");
    const form = document.getElementById('formEditar');

    // Si existe el formulario de login, se asigna el manejador correspondiente
    if(login){
        hacerLogin(login)
    }

    // Si existe el formulario de registro, se asigna el manejador correspondiente
    if(registro){
        hacerRegistro(registro)
    }
 
    // Si hay un botón o enlace al carrito, se previene el comportamiento por defecto y se llama a la función para cargar el carrito
    if(carrito){
        carrito.addEventListener('click', function (e) {
            e.preventDefault(); // Previene salto si es <a href="#">
            getCarrito();
        });    
    }

    // Si existe el botón para borrar el carrito, se asigna la función correspondiente
    if(delete_btn){
        delete_btn.addEventListener('click', function(e) {
            e.preventDefault(); // ← FALTABA LLAMAR A ESTA FUNCIÓN CON PARÉNTESIS
            borrar_items_carrito();
        })
    }

    // Si hay un botón de logout, al hacer clic redirige al endpoint de logout
    if (logout_btn) {
        logout_btn.addEventListener('click', async function () {
            try {
                const response = await fetch('/api/logout', {
                    method: 'GET',
                });
    
                if (response.ok) {
                    window.location.href = '/api/login';
                } else {
                    console.error("Fallo al cerrar sesión:", response.status);
                }
            } catch (error) {
                console.error("Error al hacer logout:", error);
            }
        });
    }
    

    // Si existe el botón para tramitar pedido
    if(tramitar_btn){
        tramitar_btn.addEventListener('click', function(e){
            // Desactiva el botón y muestra mensaje de procesamiento
            tramitar_btn.disabled = true;
            tramitar_btn.innerHTML = "Procesando...";
            // Después de 5 segundos, lo reactiva
            setTimeout(function() {
                tramitar_btn.disabled = false;
                tramitar_btn.innerHTML = "Procesar Compra";
            }, 5000);
            e.preventDefault(); // ← FALTABA LLAMAR A ESTA FUNCIÓN CON PARÉNTESIS
            tramitar_pedido(tramitar_btn);
        });
    }

    // Si hay botones para añadir productos al carrito, se asigna la función a cada uno
    if(insert_pr_btn){
        insert_pr_btn.forEach(boton => {
            insert_carrito(boton);
        });
    }

    // Si existe un formulario de edición de producto, se evita el envío por defecto y se ejecuta la lógica personalizada
    if(form){
        form.addEventListener('submit', function (e) {
            e.preventDefault(); 
            actualizarProducto();
        });
    }
});



