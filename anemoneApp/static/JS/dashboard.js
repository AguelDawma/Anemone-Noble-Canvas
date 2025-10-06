document.addEventListener('DOMContentLoaded' , function(){
    const userEmail = localStorage.getItem('currentUserEmail');
    const clientName = document.getElementById('my-username');

    if(!localStorage.getItem('isLoggedIn')){
        window.location.href = 'login.html'
        return;
    }

    const userDataString = localStorage.getItem(userEmail);
    if(userDataString){
        console.log('Data found.');
        const userData = JSON.parse(userDataString);
        clientName.textContent = userData.username;
    }
})