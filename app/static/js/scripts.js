
async function hacerLogin(login){
    login.addEventListener('submit', async(e) =>{
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        console.log(email)

        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'email': email,
                'password': password
            })
        })
        .then(response => {
            return response.json().then(data => {
                if (!response.ok) {
                    throw new Error(data.error || 'Error desconocido');
                }
                return data;
            });
        })
        .then(data => {
            localStorage.setItem('authToken', data.token);
            window.location.href = '/dashboard';
        })
        .catch(error => {
            // Aquí puedes mostrar el error con JS sin necesidad de recargar la página
            const errorDiv = document.getElementById('mensaje-error');
            errorDiv.textContent = error.message;
            errorDiv.style.display = 'block';
        });
        
    });
}

document.addEventListener('DOMContentLoaded', function(){
    const login = document.getElementById('loginForm');

    if(login){
        hacerLogin(login)
    }
});