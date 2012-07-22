from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

count = 0


@csrf_exempt
def android(request, userid=0, loc=0):
    global count
    if request.method == 'POST':
        count += 1
        return HttpResponse(count)
    m = count % 2
    return HttpResponse(m)
