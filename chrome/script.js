// Enable pusher logging - don't include this in production
Pusher.log = function(message) {
    if (window.console && window.console.log) window.console.log(message);
};

// Flash fallback logging - don't include this in production
WEB_SOCKET_DEBUG = true;

var append_notice = function(icon, message) {
    var notice = window.webkitNotifications.createNotification(
        icon, 'Tapmo.co!', message);
    notice.show();

    var el = $('<li>').html('<img src="' + icon + '"> ' + message);
    $('#notifications').append(el);
};

var pusher = new Pusher('f00bf3021b6b454ddb23');
var channel = pusher.subscribe('me@joshma.com');
channel.bind('status_change', function(data) {
    $.each(data.urls, function(i,url) {
        chrome.tabs.create({ url: url });
    });
    if (data.message.length > 0) {
        append_notice(data.icon, data.message);
    }
});


chrome.history.onVisited.addListener(function(result) {
	console.log(result);
	$.post('http://www.tapmo.co/user/me@joshma.com/history', {
		'url' : result.url
	}, function(res) {

	});
});