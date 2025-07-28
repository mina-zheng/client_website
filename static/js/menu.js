menu = document.querySelector(".menu-options");

function toggle_menu() {
    const hidden = getComputedStyle(menu).display === "none";
    if (hidden) {
        menu.style.display = "flex";
    }
    else {
        menu.style.display = "none";
    }
}