document.addEventListener('DOMContentLoaded' , function(){
    const menuIcon = document.querySelector('.menuBar');
    const mainNav = document.querySelector('.menu-nav');

    const searchIcon = document.querySelector('.search');
    const searchContainer = document.querySelector('.search-container');
    const searchInput = document.querySelector('.search-input');

    menuIcon.addEventListener('click' , function(){
        menuIcon.classList.toggle('active');
        mainNav.classList.toggle('active');
    })

    searchIcon.addEventListener('click' , function(){
        searchContainer.classList.toggle('active');
        searchIcon.classList.toggle('active');
        searchInput.classList.toggle('active');
    })
})

