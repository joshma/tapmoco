from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
import random
import string
import re

from checkin.views import check_fs_auth, get_auth_uri

SECRET_SIZE = 10
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$')


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.user and request.user.is_active:
        return redirect('hq')
    errors = {}
    email = ''
    password = ''
    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        if not email:
            errors['email'] = 'Please enter an email'
        elif not EMAIL_REGEX.match(email):
            errors['email'] = 'Invalid email'
        if not password:
            errors['password'] = 'Please enter a password'
        elif len(password) < 6:
            errors['password'] = 'Must be at least 6 characters'
        if not len(errors):
            if User.objects.filter(email=email).exists():
                user = authenticate(username=email, password=password)
                if user is not None and user.is_active:
                    login(request, user)
                    return redirect('hq')
                errors['email'] = 'Email already registered'
            else:
                User.objects.create_user(email, email, password)
                user = authenticate(username=email, password=password)
                login(request, user)
                return redirect('hq')
    d = {
        'errors': errors,
        'email': email,
        'password': password
    }
    return render(request, 'signup.html', d)


@require_POST
def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        login(request, user)
        return redirect('hq')
    messages.error(request, "Invalid username and/or password.")
    return redirect('home')


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')


@login_required
def hq(request):
    profile = request.user.get_profile()
    if not profile.secret:
        profile.secret = ''.join(random.choice(string.letters) for i in xrange(SECRET_SIZE))
        profile.save()

    # Foursquare
    fs_authorized = check_fs_auth(request.user)

    d = {
        'profile': profile,
        'fs': {
            'authorized': fs_authorized,
            'url': get_auth_uri()
        }
    }
    return render(request, 'hq.html', d)


@login_required
@require_POST
def url_update(request):
    url = request.POST.get('url', 'www.tapmo.co')
    profile = request.user.get_profile()
    profile.url = url
    profile.save()
    messages.success(request, "URL updated to <strong>%s</strong>" % url)
    return redirect('hq')
