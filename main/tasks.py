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
    url = "http://%s" % url
    print "notifying %s" % url
    params = urllib.urlencode([('username', user.username), ('loc', loc), ('status', status)])
    res = urllib2.urlopen(url, params).read()
    print "response: %s" % res
    try:
        data = json.loads(res)
    except json.decoder.JSONDecodeError:
        # Silently drop invalid responses.
        return
    out_data = {
        'urls': data.get('urls', []),
        'message': data.get('message', 'No message')
    }
    p[user.username].trigger('status_change', out_data)
