# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from DjangoRESTImage.serializers import *
from django.contrib.auth.models import User
from DjangoRESTImage.permission import * 

import json

"""
    获取所有图片信息
"""
@api_view(['GET', 'POST'])
@permission_classes((AccessPermission,))
@authentication_classes((TokenAuthentication,))
def fetch_all_image_list(request):
    print "\n\ndata:"
    print request.data
    
    images = Image.objects.all()
    serializers = ImageSerializer(images, context={'request': request}, many=True)
    try:
        print serializers.data
    except Exception,e:
        print "Open ERRPR:", e
    return Response(serializers.data)    



"""
    获取指定Project的所有图片信息
"""
@api_view(['GET', 'POST'])
@permission_classes((AccessPermission,))
@authentication_classes((TokenAuthentication,))
def fetch_project_image_list(request):
    print "\n\ndata:"
    print request.data

    pid = request.data['params']['project_id']
    try:
        project = Project.objects.get(project_id=pid)
    except Exception, e:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    images = project.images
    serializers = ImageSerializer(images, context={'request': request}, many=True)
    
    try:
        print serializers.data
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception, e:
        print "Open ERRPR:", e
    return Response(serializers.data)    
