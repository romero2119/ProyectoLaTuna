const btnAccesibilidad = document.querySelector(".btn-accesibilidad");
const menuAccesibilidad = document.getElementById("menuAccesibilidad");
let fontSize = parseInt(localStorage.getItem("fontSize")) || 100;

// Aplicar preferencias guardadas al cargar
document.documentElement.style.fontSize = fontSize + "%";
if (localStorage.getItem("darkMode") === "true") document.documentElement.classList.add("dark-mode");
if (localStorage.getItem("highContrast") === "true") document.documentElement.classList.add("high-contrast");

// Mostrar/Ocultar menú
btnAccesibilidad.addEventListener("click", (e) => {
    e.stopPropagation();
    menuAccesibilidad.style.display =
        menuAccesibilidad.style.display === "flex" ? "none" : "flex";
});

// Cerrar al hacer click FUERA
document.addEventListener("click", (e) => {
    if (!menuAccesibilidad.contains(e.target) && e.target !== btnAccesibilidad) {
        menuAccesibilidad.style.display = "none";
    }
});

// Modo oscuro
document.getElementById("modoOscuro").addEventListener("click", () => {
    document.documentElement.classList.toggle("dark-mode");
    localStorage.setItem("darkMode", document.documentElement.classList.contains("dark-mode"));
});

// Aumentar
document.getElementById("aumentar").addEventListener("click", () => {
    fontSize += 10;
    document.documentElement.style.fontSize = fontSize + "%";
    localStorage.setItem("fontSize", fontSize);
});

// Disminuir
document.getElementById("disminuir").addEventListener("click", () => {
    if (fontSize > 50) {
        fontSize -= 10;
        document.documentElement.style.fontSize = fontSize + "%";
        localStorage.setItem("fontSize", fontSize);
    }
});

// Restablecer
document.getElementById("restablecer").addEventListener("click", () => {
    fontSize = 100;
    document.documentElement.style.fontSize = "100%";
    localStorage.setItem("fontSize", 100);
});

// Alto contraste
document.getElementById("contraste").addEventListener("click", () => {
    document.documentElement.classList.toggle("high-contrast");
    localStorage.setItem("highContrast", document.documentElement.classList.contains("high-contrast"));
});