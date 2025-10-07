document.addEventListener('DOMContentLoaded', function() {
    const usernameSpan = document.getElementById('username-display');

    if (usernameSpan) {
        // 1. Read the username from the data-username attribute
        const username = usernameSpan.dataset.username; 
        
        // 2. Insert the username into the span's content
        usernameSpan.textContent = username;
    }
});