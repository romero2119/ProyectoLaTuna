const toggle = document.getElementById('toggle');
const menu   = document.getElementById('menuHamburguesa');

toggle.addEventListener('click', () => {
  toggle.classList.toggle('open');
  menu.classList.toggle('open');
});