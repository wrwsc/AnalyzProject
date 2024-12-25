document.addEventListener("DOMContentLoaded", () => {
    const burger = document.getElementById("burger");
    const sideMenu = document.getElementById("sideMenu");
    burger.addEventListener("click", () => {
        sideMenu.classList.toggle("active");
    });
});
