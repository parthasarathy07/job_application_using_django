from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Q, Avg, Count

from application.models import Application
from .models import Job
from .forms import JobForm

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from review.forms import ReviewForm

def non_superuser_required(view_func):
    return user_passes_test(lambda u: not u.is_superuser)(view_func)

def non_staff_required(view_func):
    return user_passes_test(lambda u: not u.is_staff)(view_func)

def get_jobs_with_ratings(queryset):
    jobs= queryset.select_related("company").annotate(
        average_rating=Avg("company__reviews__rating"),
        review_count=Count("company__reviews")
    )
    return attach_star_counts(jobs)


def attach_star_counts(jobs):
    for job in jobs:
        rating = job.average_rating or 0.0

        rating = max(0.0, min(rating, 5.0))

        full = int(rating) 
        fractional = rating - full
        has_half = fractional >= 0.5 
        empty = 5 - full - (1 if has_half else 0)

        # attach simple iterable lists for templates
        job.full_stars_list = list(range(full))
        job.has_half_star = has_half
        job.empty_stars_list = list(range(empty))
        job.avg_display = f"{rating:.1f}" if rating > 0 else None

    return jobs


def jobListView(request):
    jobList = get_jobs_with_ratings(Job.objects.order_by("-posted_date"))
    context = {"jobs": jobList}
    return render(request, "jobs/jobList.html", context=context)


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    back_from = request.GET.get("from", "job-list")
    company = job.company

    review_stats = company.reviews.aggregate(
        average_rating=Avg('rating'),
        review_count=Count('id')
    )

    reviews = (
        company.reviews
        .select_related('user')
        .exclude(comment__isnull=True)
        .exclude(comment__exact='')
    )

    user_review = None
    form = None

    if request.user.is_authenticated:
        user_review = company.reviews.filter(user=request.user).first()

        if request.method == "POST":
            form = ReviewForm(request.POST, instance=user_review)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.company = company
                review.save()
                return redirect('jobs:jobDetail', pk=pk)
        else:
            form = ReviewForm(instance=user_review)

    context = {
        "job": job,
        "company": company,
        "reviews": reviews,
        "form": form,
        "user_review": user_review,
        "back_from": back_from,
        "average_rating": review_stats.get('average_rating') or 0,
        "review_count": review_stats.get('review_count') or 0,
    }
    return render(request, "jobs/job_detail.html", context)

@non_superuser_required
@staff_member_required(login_url='/accounts/login/')
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

@non_superuser_required
@staff_member_required(login_url='/accounts/login/')
def edit_job(request, pk):
    job = get_object_or_404(Job, pk=pk, company=request.user.profile.company)

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            updated_job = form.save(commit=False)
            if not updated_job.location:
                updated_job.location = updated_job.company.main_location
            updated_job.save()
            return redirect('jobs:jobDetail', pk=pk)
    else:
        form = JobForm(instance=job)

    return render(request, "jobs/edit_job.html", {"form": form, "job": job})

@non_superuser_required
@staff_member_required(login_url='/accounts/login/')
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk, company=request.user.profile.company)

    if request.method == "POST":
        job.delete()
        return redirect('jobs:myPosts')

    return render(request, "jobs/confirm_delete.html", {"job": job})

def job_search(request):
    query = request.GET.get("q")
    jobs = Job.objects.all()

    if query:
        jobs = Job.objects.filter(
            Q(title__icontains=query)
            | Q(company__name__icontains=query)
            | Q(location__icontains=query)
        )
    jobs = get_jobs_with_ratings(jobs)

    return render(request, "jobs/job_search.html", {"jobs": jobs, "query": query})

@staff_member_required(login_url='/accounts/login/')
def my_posts(request):
    user = request.user

    if user.is_superuser:
        jobs_qs = Job.objects.all()
    else:
        jobs_qs = Job.objects.filter(company__profiles__user=user)
    
    jobs = jobs_qs.annotate(application_count=Count('applications'))

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
