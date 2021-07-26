from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ShortUrl(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    slug = models.CharField(max_length=50, unique=True)
    original_url = models.CharField(max_length=500)
    expired = models.BooleanField(default=False)

    def __str__(self):
        return "%s  ---  %s" % (self.original_url, self.slug)
