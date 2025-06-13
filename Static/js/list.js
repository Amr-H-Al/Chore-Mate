function selectUrgency(event, value) {
    event.preventDefault(); // Prevent default link behavior
    document.getElementById('urgency-value').value = value; // Set the urgency value
    document.getElementById('urgency-btn').innerText = value + " ▼"; // Update button text
}
function filterTasks(event, value) {
    event.preventDefault(); // Prevent default link behavior
    document.getElementById('filter-value').value = value; // Set the urgency value
    document.getElementById('filterbtn').innerText = value + " ▼"; // Update button text
}