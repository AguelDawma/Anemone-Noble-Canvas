const navLoggedOut = document.getElementById('nav-logged-out');
const navLoggedIn = document.getElementById('nav-logged-in');
const logoutButton = document.getElementById('logout-button');

// Function to simulate checking login status
function checkLoginStatus() {
    // In a real application, you'd check a cookie, local storage,
    // or make an API call to your backend here.
    // For this example, let's use a simple flag.
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'; // Simulate login state

    if (isLoggedIn) {
        navLoggedOut.style.display = 'none';
        navLoggedIn.style.display = 'flex'; // Use 'flex' or 'block' depending on your desired layout
    } else {
        navLoggedOut.style.display = 'flex';
        navLoggedIn.style.display = 'none';
    }
}

function simulateLogout() {
    
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('currentUserEmail');

    window.location.href = '../index.html';
    checkLoginStatus();
    alert('You have been logged out.');
}

// Attach event listener to the logout button
logoutButton.addEventListener('click', simulateLogout);

// Check login status when the page loads
document.addEventListener('DOMContentLoaded', checkLoginStatus);