from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required,user_passes_test


from .models import Job
from .forms import JobForm

def non_superuser_required(view_func):
    return user_passes_test(lambda u: not u.is_superuser)(view_func)

def non_staff_required(view_func):
    return user_passes_test(lambda u: not u.is_staff)(view_func)

def jobListView(request):
    jobList = Job.objects.order_by("-posted_date")
    context = {"jobs": jobList}
    return render(request, "jobs/jobList.html", context=context)


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, "jobs/job_detail.html", {"job": job})

@non_superuser_required
@staff_member_required
@login_required
def post_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user.profile.company
            if(job.location is None or job.location==""):
                job.location=job.company.main_location
            job.save()
            return redirect("jobs:jobList")
    else:
        form = JobForm()
    return render(request, "jobs/post_job.html", {"form": form})

def job_search(request):
    query = request.GET.get("q")
    if query:
        jobs = (
            Job.objects.filter(title__icontains=query)
            | Job.objects.filter(company__icontains=query)
            | Job.objects.filter(location__icontains=query)
        )
    else:
        jobs = Job.objects.all()
    return render(request, "jobs/job_search.html", {"jobs": jobs, "query": query})
