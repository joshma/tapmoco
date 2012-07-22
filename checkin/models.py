from django.db import models


class FoursquareAuthToken(models.Model):
    username = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
