# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *

class AuthorAdmin(admin.ModelAdmin):
        pass
#admin.site.register(Project, AuthorAdmin)
admin.site.register([Project, Image, Annotation, UserProfile, ])
# Register your models here.
