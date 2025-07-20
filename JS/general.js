document.addEventListener('DOMContentLoaded' , function(){
    const menuIcon = document.querySelector('.menuBar');
    const mainNav = document.querySelector('.menu-nav');

    menuIcon.addEventListener('click' , function(){
        menuIcon.classList.toggle('active');
        mainNav.classList.toggle('active');
    })
})

