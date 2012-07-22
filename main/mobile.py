from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.exceptions import DoesNotExist


@csrf_exempt
def status(request, username=None, loc=0):
    try:
        user = User.objects.get(username=username)
    except DoesNotExist:
        return HttpResponseBadRequest('invalid username!')
    profile = user.get_profile()
    if request.method == 'POST':
        profile.at_desk = not profile.at_desk
        profile.save()
    m = 1 if profile.at_desk else 0
    return HttpResponse(m)


def tabs(request, userid=0, loc=0):
    return HttpResponse('http://google.com')
