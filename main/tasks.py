from celery import task
from pushtap import p
import urllib
import urllib2
import simplejson as json


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
        pass
    out_data = {
        'urls': data.get('urls', []),
        'message': data.get('message', 'No message')
    }
    p[user.username].trigger('status_change', out_data)
