let inactivityTimeout;
const sessionTimeout = 15 * 60 * 1000;  // 15 minutes in milliseconds

// Function to reset the inactivity timer
const resetTimer = () => {
  clearTimeout(inactivityTimeout);  // Clear the previous timeout
  inactivityTimeout = setTimeout(() => {
    alert('Your session is about to expire due to Timelimit.');
    window.location.href = '/logout/';  // Redirect to the logout URL
  }, sessionTimeout);  // Set the timeout for inactivity
};

// Listen for user activity events and reset the timer
document.addEventListener('mousemove', resetTimer);  // Reset on mouse movement
document.addEventListener('keypress', resetTimer);  // Reset on key press
document.addEventListener('scroll', resetTimer);    // Reset on scroll
document.addEventListener('click', resetTimer);     // Reset on click

// Start the inactivity timer when the page loads
resetTimer();
