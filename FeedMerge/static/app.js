$(document).ready(function() {
    $('.username-input').on('input', function() {
        var input = $(this);
        var username = input.val();
        var feedType = input.attr('data-feed-type');

        if (username) {
            $.ajax({
                url: checkUsernameUrl, // Use the variable set in the HTML
                data: {
                    'username': username,
                    'feed_type': feedType
                },
                dataType: 'json',
                success: function(data) {
                    if (data.exists) {
                        input.next('.status').text('Username is occupied').css('color', 'red');
                    } else {
                        input.next('.status').text('Username is available').css('color', 'green');
                    }
                }
            });
        } else {
            input.next('.status').text('');
        }
    });
});
