document.addEventListener('DOMContentLoaded' , function(){
    const body = document.body
    const menuIcon = document.querySelector('.menuBar');
    const mainNav = document.querySelector('.menu-nav');

    menuIcon.addEventListener('click' , function(){
        menuIcon.classList.toggle('active');
        mainNav.classList.toggle('active');
        body.classList.toggle('nav-active');
    })

    document.addEventListener('click' , function(event){
            menuIcon.classList.remove('active');
            mainNav.classList.remove('active');
            body.classList.remove('nav-active');
        }
    )
})

