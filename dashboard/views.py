from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from jobs.views import get_jobs_with_ratings

def dashboardview(request):
    jobList = get_jobs_with_ratings(Job.objects.order_by("-posted_date")[:5])
    context = {"jobs": jobList}
    return render(request, 'dashboard/dashboard.html', context)
