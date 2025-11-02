from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('company', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('company__name', 'user__username', 'comment')