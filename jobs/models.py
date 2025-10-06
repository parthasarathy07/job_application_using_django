from django.db import models
from django.urls import reverse

from company.models import Company

class Job(models.Model):
    company= models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    title=models.CharField(max_length=100)
    description=models.TextField(null=True, blank=True)
    location=models.CharField(max_length=100,null=True,blank=True)
    salary=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    posted_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("jobs:jobDetail", kwargs={"pk": self.pk})
    