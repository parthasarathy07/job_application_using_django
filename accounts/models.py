from django.db import models
from django.contrib.auth.models import User
from company.models import Company

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="profiles")

    def __str__(self):
        return self.user.username