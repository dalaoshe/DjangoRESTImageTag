# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save 
import datetime
#from django.db.models.signals import post_save
#from django.dispatch import receiver
#from rest_framework.authtoken.models import Token
#@receiver(post_save, sender=User)
#def create_auth_token(sender, instance=None, created=False, **kwargs):
#    if created:
#        Token.objects.create(user=instance)

class Image(models.Model):
    image_id = models.DateTimeField(auto_now_add=True)
    image_src = models.TextField(default='')
    title = models.CharField(max_length=100, blank=True, default='')
    width = models.IntegerField()
    height = models.IntegerField()
    
    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('image_id',)

class Project(models.Model):
    project_id = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    project_type = models.CharField(max_length=100, blank=True, default='')
    creater = models.ForeignKey(User, related_name='projects_created',
            on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=True, related_name='projects_ownered',
            on_delete=models.SET_NULL)

    images = models.ManyToManyField(Image, related_name='projects',
            related_query_name='images')
    
    params = models.TextField(default='')
    
    def __unicode__(self):
        return self.title
    class Meta:
        ordering = ('project_id',)

class Annotation(models.Model):
    annotation_id = models.DateTimeField(auto_now_add=True)
    
    annotation_type = models.CharField(max_length=100, blank=True, default='')
    project = models.ForeignKey(Project, related_name='project_annotation',
            on_delete=models.CASCADE)
    image = models.ForeignKey(Image, related_name='image_annotation',
            on_delete=models.CASCADE)
    content = models.TextField(default='')
    
    def __unicode__(self):
        return self.annotation_type

    class Meta:
        unique_together=('project', 'image')
        ordering = ('annotation_id',)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    register_time = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField()
    role = models.CharField(max_length=100, blank=True, default='user')
    
    def __unicode__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):  
    if created:
        delta = datetime.timedelta(days=10)
        profile, created = UserProfile.objects.get_or_create(user=instance,
                expire_time=datetime.datetime.now() + delta
                )  

post_save.connect(create_user_profile, sender=User) 
# Create your models here.
