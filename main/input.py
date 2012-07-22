from django.http import HttpResponse

count = 0


def android(request, userid=0, loc=0):
    global count
    if request.POST:
        count += 1
    m = count % 2
    return HttpResponse(m)
