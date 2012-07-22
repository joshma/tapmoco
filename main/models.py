from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import datetime


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    at_desk = models.BooleanField(default=False)


class Application(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    reg_url = models.CharField(max_length=1000)
    check_reg_url = models.CharField(max_length=1000)
    update_url = models.CharField(max_length=1000)
    secret = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return "%s [%s]" % (self.name, self.reg_url[:20])


class AppRegistration(models.Model):
    user = models.ForeignKey(User)
    app = models.ForeignKey(Application)


class URLHistory(models.Model):
    user = models.ForeignKey(User)
    url = models.CharField(max_length=1000, blank=True)
    time_added = models.DateTimeField(auto_now_add=True, default=datetime.now())


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
