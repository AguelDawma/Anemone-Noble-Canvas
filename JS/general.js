document.addEventListener('DOMContentLoaded' , function(){
    const menuIcon = document.querySelector('.menuBar');
    console.log(menuIcon);
    const mainNav = document.querySelector('.menu-nav');

    menuIcon.addEventListener('click' , function(){
        this.classList.toggle('active');
        mainNav.classList.toggle('active');
    })
})

console.log("I am in");