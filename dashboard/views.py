from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def dashboardview(request):
    return render(request, 'dashboard/dashboard.html')
