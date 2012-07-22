from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

count = 0


@csrf_exempt
def status(request, userid=0, loc=0):
    global count
    if request.method == 'POST':
        count += 1
    m = count % 2
    return HttpResponse(m)


def tabs(request, userid=0, loc=0):
    return HttpResponse('google.com')
