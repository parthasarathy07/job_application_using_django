from django.urls import path
from . import views

app_name='jobs'

urlpatterns = [
    path('', views.jobListView, name='jobList'),
    path('search/', views.job_search, name='jobSearch'),
    path('post/', views.post_job, name='postJob'),
    path('my-posts/', views.my_posts, name='myPosts'),
    path('<int:pk>/apply/', views.apply_job, name='applyJob'),
    path('<int:pk>/applicants/pdf/', views.download_applicants_pdf, name='downloadApplicantsPDF'),
    path('<int:pk>/applicants/', views.job_applicants, name='jobApplicants'),
    path('<int:pk>/', views.job_detail, name="jobDetail"),
]