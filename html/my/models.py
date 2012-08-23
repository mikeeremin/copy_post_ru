# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class SNType(models.Model):
    code = models.CharField(max_length=10, null=False)
    title = models.CharField(max_length=255, null=False)
    read_only = models.BooleanField(default=False)
    def __unicode__(self):
        return self.title


class PostPlace(models.Model):
    sn_type = models.ForeignKey(SNType)
    user = models.ForeignKey(User)
    url = models.CharField(max_length=255)
    userid = models.BigIntegerField(default=0)
    access_token = models.TextField(default='', max_length=1000)
    access_token_secret = models.CharField(default='', max_length=1000)
    oauth_token = models.CharField(default='', max_length=1000)
    oauth_token_secret = models.CharField(default='', max_length=1000)
    login = models.CharField(max_length=255, default='')
    password = models.CharField(max_length=255, default='')
    enabled = models.BooleanField(default=True)

class Sync(models.Model):
    title = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User)
    source = models.ForeignKey(PostPlace, related_name="Sync Destination?")
    destination = models.ManyToManyField(PostPlace)
    last_sync = models.DateTimeField(auto_now=True)
    updating = models.BooleanField(default=False)

class PostItem(models.Model):
    pp = models.ForeignKey(PostPlace)
    posted = models.DateTimeField(auto_now=True)
    guid = models.CharField(max_length=255, null=False, primary_key=True)
    message = models.CharField(max_length=1000)

class UserProfile(models.Model):
    url = models.URLField()
    user = models.ForeignKey(User, unique=True)