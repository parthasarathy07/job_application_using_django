from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'location', 'description','salary']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
