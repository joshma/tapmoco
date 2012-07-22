from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import datetime


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    url = models.CharField(max_length=1000, blank=True)
    secret = models.CharField(max_length=20, blank=True)
    at_desk = models.BooleanField(default=False)


class URLHistory(models.Model):
    user = models.ForeignKey(User)
    url = models.CharField(max_length=1000, blank=True)
    time_added = models.DateField(auto_now_add=True, default=datetime.now())


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
