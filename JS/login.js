const loginForm = document.getElementById('login-form');

if(loginForm){
    loginForm.addEventListener('submit' , function(event){
        event.preventDefault();

        console.log('Login attempt');

        const email = event.target.email.value;
        const password = event.target.password.value;
        const errorMessage = document.getElementById('error-message');

        const testingEmail = 'thapelosekhonyana37@gmail.com';
        const testingPassword = 'Zimb@T@zzo07';

        if(email==testingEmail && password==testingPassword){
            console.log('Login Successful.');

            localStorage.setItem('isLoggedIn', 'true');
            localStorage.setItem('email' , email);
            localStorage.setItem('password' , password);
            
            errorMessage.textContent='';
            alert('Login Successful! Redirecting to your dashboard.');
            window.location.href = '../Pages/dashboard.html'
        }else{
            console.log('Invalid credentials');
            errorMessage.textContent = 'Invalid email or password.';
        }
    })
}else{
    console.log('Login form not found');
}
