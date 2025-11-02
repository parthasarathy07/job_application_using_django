from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Company(models.Model):
    name = models.CharField(max_length=200)
    main_location = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    