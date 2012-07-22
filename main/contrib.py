from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from tapmo_lib import tapmo


@csrf_exempt
@require_POST
def checkin(request):
    urls = []
    message = "Checked into Foursquare!"
    return HttpResponse(tapmo.build_response(urls, message))
