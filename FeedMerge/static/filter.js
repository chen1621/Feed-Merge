document.addEventListener('DOMContentLoaded', function() {
    const usernames = document.querySelectorAll('.nasa');
    const posts = document.querySelectorAll('.frame-parent4');

    usernames.forEach(user => {
        user.addEventListener('click', function(e) {
            e.preventDefault();
            const userId = this.dataset.userId;
            posts.forEach(post => {
                if (post.querySelector('.marvel1').textContent.includes(userId)) {
                    post.style.display = 'flex';  // Adjust display styles as needed
                } else {
                    post.style.display = 'none';
                }
            });
        });
    });
});
