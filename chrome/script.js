// Enable pusher logging - don't include this in production
Pusher.log = function(message) {
    if (window.console && window.console.log) window.console.log(message);
};

// Flash fallback logging - don't include this in production
WEB_SOCKET_DEBUG = true;

var pusher = new Pusher('f00bf3021b6b454ddb23');
var channel = pusher.subscribe('me@joshma.com');
channel.bind('status_change', function(data) {
    console.log(data);
});

chrome.history.onVisited.addListener(function(result) {
	console.log(result);
	$.post('http://www.tapmo.co/user/me@joshma.com/history', {
		'url' : result.url
	}, function(res) {

	});
}); 