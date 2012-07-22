// Enable pusher logging - don't include this in production
Pusher.log = function(message) {
    if (window.console && window.console.log) window.console.log(message);
};

// Flash fallback logging - don't include this in production
WEB_SOCKET_DEBUG = true;

var existing_notifications = [];
var KEY = 'notices';

var append_notice = function(icon, message, silent, read) {
    if (!silent) {
        var notice = window.webkitNotifications.createNotification(
            icon, 'Tapmo.co!', message);
        notice.show();
    }

    var cls = "unread";
    if (read) {
        cls = "read";
    }
    console.log('appending ' + message);
    var el = $('<li class="' + cls + '">').html('<img width="48" src="' + icon + '"> ' + message);
    $('#notifications').prepend(el);
    $('.empty').remove();

    if (!silent) {
        existing_notifications.push({
            'icon': icon,
            'message': message
        });
        localStorage.setItem(KEY, JSON.stringify(existing_notifications));
    }
};

if (localStorage.getItem(KEY) ===  null) {
    localStorage.setItem(KEY, JSON.stringify(existing_notifications));
} else {
    existing_notifications = JSON.parse(localStorage.getItem(KEY));
    for (var i = 0; i < existing_notifications.length; i++) {
        var notice = existing_notifications[i];
        console.log('re-appending ' + notice.message);
        append_notice(notice.icon, notice.message, true, true);
    }
}

var pusher = new Pusher('f00bf3021b6b454ddb23');
var channel = pusher.subscribe('me@joshma.com');
channel.bind('status_change', function(data) {
    $.each(data.urls, function(i,url) {
        chrome.tabs.create({ url: url });
    });
    if (data.message.length > 0) {
        append_notice(data.icon, data.message, false, false);
    }
});


chrome.history.onVisited.addListener(function(result) {
	console.log(result);
	$.post('http://www.tapmo.co/user/me@joshma.com/history', {
		'url' : result.url
	}, function(res) {

	});
});