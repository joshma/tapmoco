from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    url = models.CharField(max_length=1000, default="www.tapmo.co")
