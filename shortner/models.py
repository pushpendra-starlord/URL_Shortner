from django.db import models

# Create your models here.

class ShortUrl(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    slug = models.CharField(max_length=50, unique=True)
    original_url = models.CharField(max_length=500)
    expired = models.BooleanField(default=False)
