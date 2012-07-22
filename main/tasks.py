from celery import task
from pushtap import p
import urllib
import urllib2


@task()
def notify_status_change(user, url, loc, status):
    print "notifying %s" % url
    params = urllib.encode([('username', user.username), ('loc', loc), ('status', status)])
    urllib2.open(url, params)
