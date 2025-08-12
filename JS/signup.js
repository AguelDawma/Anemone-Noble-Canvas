const signupForm = document.getElementById('signup-form');
const usernameInput = document.getElementById('username');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('new-password');
const confirmPasswordInput = document.getElementById('confirm-password');
const errorMessage = document.getElementById('signup-errorMessage');

function validateForm(){
    const username = usernameInput.ariaValueMax.trim();
    const email = emailInput.ariaValueMax.trim();
    const password = passwordInput.ariaValueMax.trim();
    const confirmPassword = confirmPasswordInput.ariaValueMax.trim();

    errorMessage.textContent = '';

    if(password !== confirmPassword){
        errorMessage.textContent = 'Passwords do not match.';
        return;
    }

    console.log('Form is valid, signing up user...');
}

signupForm.addEventListener('submit' , function(event){
    event.preventDefault();
    validateForm();
})