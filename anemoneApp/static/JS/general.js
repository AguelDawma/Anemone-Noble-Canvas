function confirmLogout(){
    if(confirm("Are you sure you want to log out?")){
        document.getElementById('logout_form').submit();
    }
}

document.addEventListener('DOMContentLoaded', function () {

    const usernameSpan = document.querySelector('.username-display');

    if (usernameSpan) {
        // 1. Read the username from the data-username attribute
        const username = usernameSpan.dataset.username; 
        
        // 2. Insert the username into the span's content
        usernameSpan.textContent = username;
    }

    const body = document.body;
    const menuIcon = document.querySelector('.menuBar');
    const mainNav = document.querySelector('.menu-nav');
    const sideMenu = document.querySelector('.side-menu-container');
    const overlay = document.querySelector('.overlay');
    const close_btn = document.querySelector('.nav-close-btn');

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
        overlay.classList.toggle('active');
        close_btn.classList.toggle('active');
    });

    // Close the menu when clicking outside of the side menu container
    document.addEventListener('click', function (event) {
        if (sideMenu && sideMenu.contains(event.target)) return; // click inside menu -> ignore
        menuIcon.classList.remove('active');
        mainNav.classList.remove('active');
        body.classList.remove('nav-active');
        overlay.classList.remove('active');
        close_btn.classList.remove('active')
    });
});

