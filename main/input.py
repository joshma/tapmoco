from django.shortcuts import render
from django.http import HttpResponse

count = 0


def android(request, userid=0, loc=0):
    global count
    count += 1
    return HttpResponse('userid=%s, loc=%s, count=%d' % (userid, loc, count))
