from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import random
import string
import pusher

pusher.app_id = '24415'
pusher.key = 'f00bf3021b6b454ddb23'
pusher.secret = 'e03efec23cce19d45ca1'

SECRET_SIZE = 10


def home(request):
    return render(request, 'home.html')


def signup(request):
    return render(request, 'signup.html')


@require_POST
def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        login(request, user)
        return redirect('hq')
    return redirect('home')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def hq(request):
    profile = request.user.get_profile()
    if profile.secret == '':
        profile.secret = ''.join(random.choice(string.letters) for i in xrange(SECRET_SIZE))
        profile.save()
    d = {
        'profile': profile
    }
    return render(request, 'hq.html', d)


@login_required
@require_POST
def url_update(request):
    url = request.POST.get('url', 'www.tapmo.co')
    profile = request.user.get_profile()
    profile.url = url
    profile.save()
    return redirect('hq')
