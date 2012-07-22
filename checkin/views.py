from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import reverse
from tapmo_lib import tapmo

from checkin.models import FoursquareAuthToken

CLIENT_ID = 'CRSPZPSVFVRZBHKPGCO50T1P0O4M0LSTCCIIPHUU002WGD2P'
CLIENT_SECRET = 'VHXJCVYDPWMDBKDK0ZJ22OZBCIPTWKETBPBPXZ12AKX1HTYH'
CALLBACK_URL = reverse('checkin_callback')


def check_fs_auth(user):
    return FoursquareAuthToken.objects.filter(user=user).exists()


@csrf_exempt
@require_POST
def checkin(request):
    urls = []
    message = "Checked into Foursquare!"
    return HttpResponse(tapmo.build_response(urls, message))
