document.addEventListener("DOMContentLoaded", function() {
    // Check if there are any flash messages
    const flashMessages = document.getElementById('flashMessages');
    if (flashMessages && flashMessages.dataset.message) {
        const message = flashMessages.dataset.message;
        const category = flashMessages.dataset.category;

        // Show custom alert based on the message category (e.g., 'danger' for errors)
        showAlert(message, category);
    }
});

function showAlert(message, category) {
    const alertBox = document.createElement('div');
    alertBox.classList.add('alert');
    
    if (category === 'danger') {
        alertBox.classList.add('alert-danger'); // Red alert for error
    } else {
        alertBox.classList.add('alert-success'); // Green alert for success
    }

    alertBox.textContent = message;
    document.body.prepend(alertBox); // Show alert at the top of the page

    // Automatically hide alert after 5 seconds
    setTimeout(() => alertBox.remove(), 5000);
}
