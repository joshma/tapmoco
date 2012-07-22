from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from tapmo_lib import tapmo
from webmo.settings import HOSTNAME
import os
import urllib
import urllib2
import simplejson as json

from checkin.models import FoursquareAuthToken

CLIENT_ID = os.environ.get('FS_CLIENT_ID', '0R0DSOBI41PMKH3FFI1REOB14EWCTELNNGDHXX1CJK5R2HU2')
CLIENT_SECRET = os.environ.get('FS_CLIENT_SECRET', '5AWHXKMHP1Q55DMK4AXN4NU0CG4XVL2GROFPI3LASYDJHWRR')
CALLBACK_URL = reverse_lazy('checkin_callback')


def check_fs_auth(user):
    return FoursquareAuthToken.objects.filter(user=user).exists()


def get_auth_uri():
    redirect_uri = get_redirect_uri()
    return "https://foursquare.com/oauth2/authenticate?client_id=%s&response_type=code&redirect_uri=%s" % (CLIENT_ID, redirect_uri)


def get_redirect_uri():
    return "http://%s%s" % (HOSTNAME, CALLBACK_URL)


@csrf_exempt
@require_POST
def notify(request):
    urls = []
    status = request.POST.get('status', '0')
    message = ""
    icon = None
    if status == '1':
        checkin_url = "https://api.foursquare.com/v2/checkins/add"
        # Yay hard-code Dropbox
        username = request.POST.get('username', None)
        if not username:
            return HttpResponseBadRequest('bad username')
        auth_token = FoursquareAuthToken.objects.get(username=username)
        params = urllib.urlencode([
            ('oauth_token', auth_token.token),
            ('venueId', '4f3970aee4b08f009b927739'),
            ('shout', 'An NFC generated checkin for Greylock hackfest!'),
            ('broadcast', 'public,twitter'),
        ])
        print "POST:\n%s\n%s" % (checkin_url, params)
        urllib2.urlopen(checkin_url, params)

        icon = get_photo_url(auth_token.token)

        message = "Checked into Foursquare!"
    if icon:
        out = tapmo.build_response(urls, message, icon)
    else:
        out = tapmo.build_response(urls, message)
    return HttpResponse(out)


def get_photo_url(auth_token):
    url = "https://api.foursquare.com/v2/users/self"
    params = urllib.urlencode([('oauth_token', auth_token)])
    print "POST:\n%s\n%s" % (url, params)
    res = urllib2.urlopen(url, params).read()
    print "received res:" % res
    res_data = json.loads(res)
    photo = res_data['response']['user']['photo']
    return "%s48x48%s" % (photo['prefix'], photo['suffix'])


@login_required
def callback(request):
    code = request.GET.get('code', None)
    if not code:
        return HttpResponseBadRequest('invalid code')
    fs_url = "https://foursquare.com/oauth2/access_token?client_id=%s&client_secret=%s&grant_type=authorization_code&redirect_uri=%s&code=%s" \
        % (CLIENT_ID, CLIENT_SECRET, get_redirect_uri(), code)
    print fs_url
    res = urllib2.urlopen(fs_url).read()
    res_data = json.loads(res)
    print res_data
    if FoursquareAuthToken.objects.filter(username=request.user.username).exists():
        FoursquareAuthToken.objects.filter(username=request.user.username).delete()
    auth_token = FoursquareAuthToken(username=request.user.username, token=res_data['access_token'])
    auth_token.save()
    return redirect('hq')
