from django.shortcuts import render
from django.http import HttpResponse


def android(request, userid=0, loc=0):
    return HttpResponse('userid=%s, loc=%s' % (userid, loc))
