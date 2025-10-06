# accounts/views.py
from django.shortcuts import render, redirect
from django.urls import resolve
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

from .forms import StaffSignUpForm, NormalUserSignUpForm
from django.contrib.auth import logout

def staff_signup(request):
    if request.method == 'POST':
        form = StaffSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = StaffSignUpForm()
    return render(request, 'registration/staff_signup.html', {'form': form})


def normal_signup(request):
    if request.method == 'POST':
        form = NormalUserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = NormalUserSignUpForm()
    return render(request, 'registration/normal_signup.html', {'form': form})

def custom_logout(request):
    logout(request)

    next_url = request.GET.get('next')

    default_redirect = '/'

    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        try:
            resolver_match = resolve(next_url)
            view_func = resolver_match.func

            if hasattr(view_func, 'login_url') or getattr(view_func, 'login_required', False):
                return redirect(f"{settings.LOGIN_URL}?next={next_url}")

            return redirect(next_url)

        except Exception:
            return redirect(default_redirect)

    return render(request, 'registration/logged_out.html')