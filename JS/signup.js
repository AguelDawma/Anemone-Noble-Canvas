const signupForm = document.getElementById('signup-form');
const usernameInput = document.getElementById('username');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('new-password');
const confirmPasswordInput = document.getElementById('confirm-password');
const errorMessage = document.getElementById('signup-error-message');

function validateForm(){
    const username = usernameInput.value.trim();
    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();
    const confirmPassword = confirmPasswordInput.value.trim();

    errorMessage.textContent = '';

    if(password !== confirmPassword){
        errorMessage.textContent = 'Passwords do not match.';
        return;
    }

    console.log('Form is valid, signing up user...');
}

function signup(){
    errorMessage.textContent = 'Signing up user...';
    
    localStorage.setItem(email+'name' , username);
    localStorage.setItem(email+'email' , email);
    localStorage.setItem(email+'isSignedIn' , 'true');

    window.location.href = '../Pages/login.html';
}

signupForm.addEventListener('submit' , function(event){
    event.preventDefault();
    validateForm();
    signup();
})