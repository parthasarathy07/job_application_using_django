from django.contrib import admin
from .models import Company
from jobs.models import Company, Job

class JobInline(admin.TabularInline):
    model = Job
    extra = 1
    fields = ('title', 'description', 'location', 'salary',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'main_location', 'website')  
    search_fields = ('name', 'main_location')                
    list_filter = ('main_location',)                     
    ordering = ('name',)
    inlines = [JobInline]                                
