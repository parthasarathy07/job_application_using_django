from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'applied_date')
    list_filter = ('applied_date', 'job')
    search_fields = ('user__username', 'user__email', 'job__title')
    ordering = ('-applied_date',)
    date_hierarchy = 'applied_date'
    list_per_page = 25
    readonly_fields = ('applied_date',)
    fieldsets = (
        ('Applicant Info', {
            'fields': ('user', 'job')
        }),
        ('Metadata', {
            'fields': ('applied_date',),
            'classes': ('collapse',),
        }),
    )
