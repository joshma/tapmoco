from celery import task
import urllib
import urllib2
import simplejson as json
import pusher

pusher.app_id = '24415'
pusher.key = 'f00bf3021b6b454ddb23'
pusher.secret = 'e03efec23cce19d45ca1'
p = pusher.Pusher()


@task()
def notify_status_change(user, url, loc, status):
    print "notifying %s" % url
    params = urllib.urlencode([('loc', loc), ('status', status)])
    try:
        res = urllib2.urlopen(url, params).read()
    except urllib2.HTTPError as http_error:
        res = http_error.read()
        with open('/Users/joshma/error.html', 'w+') as f:
            f.write(res)
    print "response: %s" % res
    try:
        data = json.loads(res)
    except json.decoder.JSONDecodeError:
        # Silently drop invalid responses.
        return
    out_data = {
        'urls': data.get('urls', []),
        'message': data.get('message', 'No message'),
        'icon': data.get('icon', '48.png')
    }
    p[user.username].trigger('status_change', out_data)
