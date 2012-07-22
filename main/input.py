from django.views.decorators.http import require_POST
from django.http import HttpResponse

count = 0


@require_POST
def android(request, userid=0, loc=0):
    global count
    count += 1
    m = count % 2
    return HttpResponse(m)
