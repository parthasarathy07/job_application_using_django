from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from jobs.models import Job

def dashboardview(request):
    jobList = Job.objects.order_by("-posted_date")[:5]
    context = {"jobs": jobList}
    return render(request, 'dashboard/dashboard.html', context)
