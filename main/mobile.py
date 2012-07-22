from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from tasks import notify_status_change


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
        notify_status_change.delay(user)
        profile.save()
    m = 1 if profile.at_desk else 0
    return HttpResponse(m)


def tabs(request, username=None, loc=0):
    return HttpResponse('http://google.com')