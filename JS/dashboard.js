document.addEventListener('DOMContentLoaded' , function(){
    const myUsername = localStorage.getItem('email');
    const clientName = document.getElementById('my-username');

    clientName.textContent = myUsername;
})