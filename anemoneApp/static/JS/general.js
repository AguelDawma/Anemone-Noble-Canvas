document.addEventListener('DOMContentLoaded', function () {
    const body = document.body;
    const menuIcon = document.querySelector('.menuBar');
    const mainNav = document.querySelector('.menu-nav');
    const sideMenu = document.querySelector('.side-menu-container');

    // Safety: if elements aren't present, do nothing
    if (!menuIcon || !mainNav) {
        console.log('menu: required elements not found', { menuIcon, mainNav });
        return;
    }

    menuIcon.addEventListener('click', function (event) {
        // Prevent the click from bubbling up to document and immediately closing the menu
        event.stopPropagation();
        menuIcon.classList.toggle('active');
        mainNav.classList.toggle('active');
        body.classList.toggle('nav-active');
    });

    // Close the menu when clicking outside of the side menu container
    document.addEventListener('click', function (event) {
        if (sideMenu && sideMenu.contains(event.target)) return; // click inside menu -> ignore
        menuIcon.classList.remove('active');
        mainNav.classList.remove('active');
        body.classList.remove('nav-active');
    });
});

