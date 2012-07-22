// Enable pusher logging - don't include this in production
Pusher.log = function(message) {
    if (window.console && window.console.log) window.console.log(message);
};

// Flash fallback logging - don't include this in production
WEB_SOCKET_DEBUG = true;

var pusher = new Pusher('f00bf3021b6b454ddb23');
var channel = pusher.subscribe('me@joshma.com');
channel.bind('status_change', function(data) {
    $.each(data.urls, function(i,url) {
        chrome.tabs.create({ url: url });
    });
    if (data.message.length > 0) {
        var notice = window.webkitNotifications.createNotification(
            '48.png', 'Tapmo.co!', data.message);
        notice.show();
    }
});


chrome.history.onVisited.addListener(function(result) {
	console.log(result);
	$.post('http://www.tapmo.co/user/me@joshma.com/history', {
		'url' : result.url
	}, function(res) {

	});
});