from django.urls import path
from . import views

app_name = 'company'

urlpatterns = [
    path('create/', views.create_company, name='create'),
]