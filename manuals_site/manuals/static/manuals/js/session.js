// Display assignment notice message if user has overdue/due-soon assignments
// Only display these message at beginning of the session

let assignment_alert = document.getElementById('assignment-alert');

if (!sessionStorage.getItem('notified')) {
    assignment_alert.style.display = 'block';
    sessionStorage.setItem('notified', true);
}