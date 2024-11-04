// Selección de elementos de HTML
const formOpenBtn = document.querySelector("#form-open"),
    signupOpenBtn = document.querySelector("#signup-open"), // Botón de registro
    home = document.querySelector(".home"),
    formContainer = document.querySelector(".form_container"),
    formCloseBtn = document.querySelector(".form_close"),
    loginForm = document.querySelector(".login_form"),
    signupForm = document.querySelector(".signup_form"),
    pwShowHide = document.querySelectorAll(".pw_hide");

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

// Mostrar/Ocultar contraseña

pwShowHide.forEach((icon) => {
    icon.addEventListener("click", () => {
        // Selecciona el campo de contraseña que está en el mismo contenedor
        let passwordField = icon.parentElement.querySelector("input[type='password'], input[type='text']");

        if (passwordField.type === "password") {
            passwordField.type = "text";
            icon.classList.replace("uil-eye-slash", "uil-eye");
        } else {
            passwordField.type = "password";
            icon.classList.replace("uil-eye", "uil-eye-slash");
        }
    });
});


// Formulario de Registro
document.addEventListener("DOMContentLoaded", () => {
    const formContainer = document.querySelector(".form-container");
    formContainer.style.opacity = "0";
    formContainer.style.transform = "translateY(20px)";
    
    setTimeout(() => {
        formContainer.style.transition = "opacity 0.5s ease, transform 0.5s ease";
        formContainer.style.opacity = "1";
        formContainer.style.transform = "translateY(0)";
    }, 100);
});


// Menú desplegable
document.querySelector(".menu-toggle").addEventListener("click", () => {
    const sidebar = document.querySelector(".sidebar");
    sidebar.classList.toggle("collapsed");

    const formContainer = document.querySelector(".form-container");
    if (sidebar.classList.contains("collapsed")) {
        formContainer.style.marginLeft = "60px"; // Ajusta margen cuando el menú está colapsado
    } else {
        formContainer.style.marginLeft = "220px"; // Ajusta margen cuando el menú está expandido
    }
});