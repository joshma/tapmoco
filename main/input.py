from django.http import HttpResponse

count = 0


def android(request, userid=0, loc=0):
    global count
    if request.method == 'POST':
        count += 1
        return HttpResponse(count)
    m = count % 2
    return HttpResponse(m)
