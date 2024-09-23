// Funciones para mostrar y ocultar el menú
document.getElementById("btn_menu")?.addEventListener("click", mostrar_menu);
document.getElementById("back_menu")?.addEventListener("click", ocultar_menu);

const nav = document.getElementById("nav");
const background_menu = document.getElementById("back_menu");

function mostrar_menu() {
    nav.style.right = "0px";
    background_menu.style.display = "block";
}

function ocultar_menu() {
    nav.style.right = "-250px";
    background_menu.style.display = "none";
}

// JavaScript para alternar el modo
const toggleButton = document.getElementById('theme-toggle');
if (toggleButton) {
    toggleButton.addEventListener('click', () => {
        if (document.body.dataset.theme === 'dark') {
            document.body.dataset.theme = 'light';
            localStorage.setItem('theme', 'light');
        } else {
            document.body.dataset.theme = 'dark';
            localStorage.setItem('theme', 'dark');
        }
    });
}

// Cargar la preferencia del usuario al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.body.dataset.theme = savedTheme;
    }
});
document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('theme-toggle');
    let currentTheme = localStorage.getItem('theme') || 'light';

    // Aplica el tema actual
    document.body.setAttribute('data-theme', currentTheme);

    // Cambia entre los modos claro y oscuro
    toggleButton.addEventListener('click', () => {
        currentTheme = currentTheme === 'light' ? 'dark' : 'light';
        document.body.setAttribute('data-theme', currentTheme);
        localStorage.setItem('theme', currentTheme);
    });
});