from django.urls import path
from . import views

app_name='jobs'

urlpatterns = [
    path('', views.jobListView, name='jobList'),
    path('search/', views.job_search, name='jobSearch'),
    path('post/', views.post_job, name='postJob'),
    path('my-posts/', views.my_posts, name='myPosts'),
    path('<int:pk>/', views.job_detail, name="jobDetail"),
]