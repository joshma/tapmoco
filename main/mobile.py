from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST

from tasks import notify_status_change
from models import UserProfile, URLHistory


@csrf_exempt
def status(request, username=None, loc=0):
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('invalid username!')
    profile = user.get_profile()
    if request.method == 'POST':
        profile.at_desk = not profile.at_desk

        print 'Starting task to notify services of status change'
        urls = [d['url'] for d in UserProfile.objects.filter(url__isnull=False).values('url')]
        urls = filter(lambda n: len(n) > 0, urls)
        for url in urls:
            notify_status_change.delay(user, url)
        profile.save()
    m = 1 if profile.at_desk else 0
    return HttpResponse(m)


def tabs(request, username=None, loc=0):
    return HttpResponse('http://google.com')


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
