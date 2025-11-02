from django.db import models
from django.conf import settings
from company.models import Company
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_written')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('company', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company.name} - {self.user.username} ({self.rating}★)"
