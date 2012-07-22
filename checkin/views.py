from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from tapmo_lib import tapmo
from webmo.settings import HOSTNAME
import os
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
def checkin(request):
    urls = []
    message = "Checked into Foursquare!"
    return HttpResponse(tapmo.build_response(urls, message))


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
    auth_token = FoursquareAuthToken(user=request.user, token=res_data['access_token'])
    auth_token.save()
    return redirect('hq')
