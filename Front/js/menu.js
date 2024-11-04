// Función para cargar el menú desde el archivo HTML
function loadMenu() {
    fetch('menu.html') // Cambia la ruta si es necesario
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(data => {
            document.getElementById('menu-container').innerHTML = data;
            attachMenuToggle(); // Llama a la función para agregar el evento del icono
        })
        .catch(error => console.error('Error al cargar el menú:', error));
}

// Función para agregar el evento de toggle al menú
function attachMenuToggle() {
    const menuIcon = document.getElementById('menu-icon');
    const menuList = document.getElementById('menu-list');

    menuIcon.addEventListener('click', () => {
        // Alternar la visibilidad del menú
        menuList.style.display = menuList.style.display === 'none' ? 'block' : 'none';
    });
}

// Carga el menú al iniciar la página
window.onload = loadMenu;
