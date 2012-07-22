from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def home(request):
    return render(request, 'home.html')


def signup(request):
    return render(request, 'signup.html')


@require_POST
def login_view(request):
    # WOO HARDCODED LOGIN
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
    return render(request, 'hq.html')
