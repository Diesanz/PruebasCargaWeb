

function getCarrito() {
    // Redirige directamente a la ruta del carrito
    // El navegador se encargará de enviar automáticamente las cookies con el token
    window.location.href = '/api/carrito';
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


document.addEventListener('DOMContentLoaded', function(){
    const login = document.getElementById('loginForm');
    const userIcon = document.getElementById('userIcon')
    const carrito = document.getElementById('carrito')

    if(login){
        hacerLogin(login)
    }
    
    if (userIcon) {
        // Evento para manejar el clic en el ícono
        userIcon.addEventListener('click', function() {
            // Si no hay token, redirige al login
            window.location.href = '/api/login';
        });
    }

    if(carrito){
        carrito.addEventListener('click', function (e) {
            e.preventDefault(); // Previene salto si es <a href="#">
            getCarrito();
        });    
    }
});