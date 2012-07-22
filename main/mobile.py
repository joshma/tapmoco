from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST

from tasks import notify_status_change
from models import URLHistory, AppRegistration, UserProfile


@csrf_exempt
def status(request, username=None, loc=0):
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('invalid username!')
    profile = user.get_profile()
    m = 1 if profile.at_desk else 0
    if request.method == 'POST':
        profile.at_desk = not profile.at_desk

        print 'Starting task to notify services of status change'
        apps = [ar.app for ar in AppRegistration.objects.filter(user=user)]
        urls = [app.update_url for app in apps]
        m = 1 if profile.at_desk else 0
        for url in urls:
            url = url % username
            notify_status_change.delay(user, url, loc, m)
        profile.save()
    return HttpResponse(m)


def tabs(request, username=None, loc=0):
    url = URLHistory.objects.latest('time_added')
    return HttpResponse(url.url)


@csrf_exempt
@require_POST
def history(request, username=None):
    url = request.POST.get('url', None)
    if not url:
        return HttpResponseBadRequest('URL missing')
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('invalid username!')
    url_history = URLHistory(url=url, user=user)
    url_history.save()
    return HttpResponse('URL successfully saved')


@csrf_exempt
def auth(request, auth_token=None):
    if not auth_token:
        return HttpResponseBadRequest('auth token missing')
    try:
        user = UserProfile.objects.get(auth_token=auth_token)
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('could not find user with that auth token')
    return HttpResponse('Success:'+user.user.email)
