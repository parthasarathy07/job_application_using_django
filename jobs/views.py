from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Q

from application.models import Application
from .models import Job
from .forms import JobForm

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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
    back_from = request.GET.get("from", "job-list")
    return render(request, "jobs/job_detail.html", {"job": job, "back_from": back_from})

@non_superuser_required
@staff_member_required(login_url='/accounts/login/')
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
    jobs = Job.objects.all()

    if query:
        jobs = Job.objects.filter(
            Q(title__icontains=query)
            | Q(company__name__icontains=query)
            | Q(location__icontains=query)
        )

    return render(request, "jobs/job_search.html", {"jobs": jobs, "query": query})

@staff_member_required(login_url='/accounts/login/')
@login_required
def my_posts(request):
    user = request.user

    if user.is_superuser:
        jobs = Job.objects.all()
    else:
        jobs = Job.objects.filter(company__profiles__user=user)

    context = {'jobs': jobs}
    return render(request, 'jobs/my_posts.html', context)

@non_superuser_required
@non_staff_required
@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    Application.objects.get_or_create(user=request.user, job=job)
    return redirect('jobs:jobList')

@staff_member_required
def job_applicants(request, pk):
    job = get_object_or_404(Job, pk=pk)
    applications = job.applications.select_related('user').order_by('-applied_date')
    return render(request, 'jobs/job_applicants.html', {'job': job, 'applications': applications})

@staff_member_required
def download_applicants_pdf(request, pk):
    job = get_object_or_404(Job, pk=pk)
    applications = job.applications.select_related('user').order_by('-applied_date')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{job.title}_applicants.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, 750, f"Applicants for {job.title}")
    p.setFont("Helvetica", 12)

    y = 720
    for app in applications:
        p.drawString(50, y, f"Name: {app.user.username}")
        p.drawString(200, y, f"Email: {app.user.email}")
        p.drawString(400, y, f"Date: {app.applied_date.strftime('%Y-%m-%d %H:%M')}")
        y -= 20
        if y < 50:
            p.showPage()
            y = 750

    p.save()
    return response
