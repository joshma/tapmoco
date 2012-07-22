from django.db import models
from django.contrib.auth.models import User


class FoursquareAuthToken(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=100)
