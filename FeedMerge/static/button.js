// JavaScript code to toggle active class on button click
document.addEventListener('DOMContentLoaded', function() {
    // Select all buttons by class name
    var buttons = document.querySelectorAll('.vector-parent, .vector-group');

    // Add click event listener to each button
    buttons.forEach(function(button) {
        button.addEventListener('click', function() {
            // First, remove 'active' class from all buttons
            buttons.forEach(function(btn) {
                btn.classList.remove('active');
            });

            // Then, add 'active' class to the clicked button
            this.classList.add('active');
        });
    });
});
