document.addEventListener('DOMContentLoaded' , function(){
    if(localStorage.getItem('isLoggedIn')){
        window.location.href = '/dashboard/';
        return;
    }

    const back = document.getElementById('back-arrow');
    back.addEventListener('click' , function(){
        window.location.href = '/';
    });
});
