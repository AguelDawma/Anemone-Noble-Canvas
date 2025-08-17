document.addEventListener('DOMContentLoaded' , function(){
    if(localStorage.getItem('isLoggedIn')){
        window.location.href = 'dashboard,html';
        return;
    }

    const loginForm = document.getElementById('login-form');

    if(loginForm){
        loginForm.addEventListener('submit' , function(event){
            event.preventDefault();

            console.log('Login attempt');

            const email = event.target.email.value;
            const password = event.target.password.value;
            const errorMessage = document.getElementById('error-message');

            const userDataString = localStorage.getItem(email);
            if(userDataString){
                console.log('Data found.');
                const userData = JSON.parse(userDataString);

                if(userData.password === password){
                    localStorage.setItem('isLoggedIn' , 'true');
                    localStorage.setItem('currentUserEmail' , email);

                    errorMessage.textContent='';
                    alert('Login Successful! Redirecting to your dashboard.');
                    window.location.href = '../Pages/dashboard.html'
                }else{
                    console.log('Invalid credentials');
                    errorMessage.textContent = 'Invalid email or password.';
                }
            }else{
                errorMessage.textContent = 'User not found, please sign up...';
            }
        });
    }else{
        console.log('Login form not found');
    }
})
        
