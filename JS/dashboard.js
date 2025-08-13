document.addEventListener('DOMContentLoaded' , function(){
    const myUsername = localStorage.getItem('name');
    const clientName = document.getElementById('my-username');

    clientName.textContent = myUsername;
})