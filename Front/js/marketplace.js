// Mostrar el producto seleccionado en pantalla completa
document.querySelectorAll('.item').forEach((item) => {
    item.addEventListener('click', () => {
        // Obtener detalles del producto seleccionado
        const imageSrc = item.querySelector('img').src;
        const descriptionText = item.querySelector('.description').textContent;
        const priceText = item.querySelector('.price').textContent;
        const locationText = item.querySelector('.location').textContent;

        // Actualizar el cuadro de pantalla completa con los detalles
        document.getElementById('full-screen-img').src = imageSrc;
        document.getElementById('full-screen-title').innerText = descriptionText;
        document.getElementById('full-screen-description').innerText = "Ubicación: " + locationText;
        document.getElementById('full-screen-price').innerText = priceText;

        // Mostrar el cuadro de pantalla completa
        document.getElementById('full-screen-product').style.display = "flex";
    });
});

// Cerrar el cuadro de pantalla completa
document.getElementById('full-screen-close').addEventListener('click', () => {
    document.getElementById('full-screen-product').style.display = "none";
});

// Evento para mostrar el formulario de inicio de sesión
formOpenBtn.addEventListener("click", () => {
    home.classList.add("show");
    loginForm.style.display = "block"; // Muestra el formulario de inicio de sesión
    signupForm.style.display = "none"; // Oculta el formulario de registro
});

// Evento para mostrar el formulario de registro
signupOpenBtn.addEventListener("click", () => {
    home.classList.add("show");
    loginForm.style.display = "none"; // Oculta el formulario de inicio de sesión
    signupForm.style.display = "block"; // Muestra el formulario de registro
});

// Evento para cerrar el formulario
formCloseBtn.addEventListener("click", () => home.classList.remove("show"));
