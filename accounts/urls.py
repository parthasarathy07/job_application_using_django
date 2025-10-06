from django.urls import path
from . import views


urlpatterns = [
    path('signup/employer/', views.staff_signup, name='staff_signup'),
    path('signup/employee/', views.normal_signup, name='normal_signup'),
    path("logout/", views.custom_logout, name="logout"),
]