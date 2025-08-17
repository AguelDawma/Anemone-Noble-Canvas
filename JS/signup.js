const signupForm = document.getElementById('signup-form');
const usernameInput = document.getElementById('signupUsername');
const emailInput = document.getElementById('signupEmail');
const passwordInput = document.getElementById('new-password');
const confirmPasswordInput = document.getElementById('confirm-password');
const errorMessage = document.getElementById('signup-error-message');

function signup(){

    const username = usernameInput.value.trim();
    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();
    const confirmPassword = confirmPasswordInput.value.trim();

    errorMessage.textContent = '';

    if(password !== confirmPassword){
        errorMessage.textContent = 'Passwords do not match.';
        return;
    }else{
        console.log('Form is valid, signing up user...');
        errorMessage.textContent = 'Validation Complete!';
    }

    if(localStorage.getItem(email)){
        errorMessage.textContent = 'User already exists, please login...';
        return;
    }
    errorMessage.textContent = 'Signing up user...';

    const userData = {
        username: username,
        password: password
    };

    localStorage.setItem(email , JSON.stringify(userData));
    
    window.location.href = '../Pages/login.html';
}

signupForm.addEventListener('submit' , function(event){
    event.preventDefault();
    signup();
})