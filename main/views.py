from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from main.models import Application, AppRegistration
from webmo.settings import HOSTNAME
import os
import random
import string
import re
import urllib2
import simplejson as json

SECRET_SIZE = 20
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


def generate_secret():
    return ''.join(random.choice(string.letters) for i in xrange(SECRET_SIZE))


def build_market_app(username):
    def out(application):
        try:
            url = application.check_reg_url % username
            url = fix_url(url)
            print "checking out %s" % url
            res = urllib2.urlopen(url).read()
        except urllib2.HTTPError:
            print "ERROR"
            res = json.dumps({'valid': False})
        print "res: %s" % res
        res_data = json.loads(res)
        registered = res_data['valid']
        print "registered: %s" % registered
        return {
            'url': application.reg_url % username,
            'name': application.name,
            'registered': registered,
            'application': application,
            'owner': application.owner.username
        }
    return out


def fix_url(url):
    # Replace references to HOSTNAME with localhost:$PORT
    desired_match = "http://%s/" % HOSTNAME
    replacement = "http://localhost:%s/" % (os.environ.get('PORT', '8000'))
    if url[:len(desired_match)] == desired_match:
        url = replacement + url[len(desired_match):]
    return url


@login_required
def hq(request):
    applications = Application.objects.filter(owner=request.user)

    market_apps = map(build_market_app(request.user.username), Application.objects.all())

    # We need to actually save which ones are registered too.
    AppRegistration.objects.filter(user=request.user).delete()
    for market_app in market_apps:
        if market_app.get('registered', False):
            ar = AppRegistration(user=request.user, app=market_app['application'])
            ar.save()

    d = {
        'market_apps': market_apps,
        'applications': applications
    }
    return render(request, 'hq.html', d)


@login_required
@require_POST
def create_application(request):
    name = request.POST.get('name', None)
    reg_url = request.POST.get('register-url', None)
    check_reg_url = request.POST.get('check-register-url', None)
    update_url = request.POST.get('update-url', None)

    if not (name and reg_url and check_reg_url and update_url):
        messages.error(request, "Please fill out all fields.")
        return redirect('hq')

    reg_url = "http://" + reg_url
    check_reg_url = "http://" + check_reg_url
    update_url = "http://" + update_url

    app = Application(owner=request.user, name=name, reg_url=reg_url,
        check_reg_url=check_reg_url, update_url=update_url,
        secret=generate_secret())
    app.save()

    messages.success(request, "Your application %s was created." % name)
    return redirect('hq')


@login_required
@require_POST
def delete_application(request):
    application = Application.objects.get(id=request.POST.get('id', None))
    if application:
        application.delete()
    messages.success(request, "Application %s successfully deleted." % application.name)
    return redirect('hq')


@login_required
def auth_view(request):
    secret = generate_secret()
    profile = request.user.get_profile()
    profile.auth_token = secret
    profile.save()
    url = 'https://chart.googleapis.com/chart?chs=300x300&cht=qr&chl=http://www.tapmo.co/auth/'+secret
    d = {
        'url': url
    }
    return render(request, 'auth.html', d)
