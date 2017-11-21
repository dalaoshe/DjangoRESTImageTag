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
    获取所有Project信息
"""
@api_view(['GET', 'POST'])
@permission_classes((AccessPermission,))
@authentication_classes((TokenAuthentication,))
def fetch_all_project_list(request):
    print "\n\ndata:"
    print request.data
    projects = Project.objects.all()
    serializers = ProjectSerializer(projects, context={'request': request}, many=True)
    try:
        print serializers.data
    except Exception,e:
        print "Open ERRPR:", e
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(serializers.data)    


"""
    获取用户被分配的所有Project信息
"""
@api_view(['GET', 'POST'])
@permission_classes((AccessPermission,))
@authentication_classes((TokenAuthentication,))
def fetch_request_user_project_list(request):
    print "\n\ndata:"
    print request.data
    
    projects = request.user.projects_ownered
    serializers = ProjectSerializer(projects, context={'request': request}, many=True)
    try:
        print serializers.data
    except Exception,e:
        print "Open ERRPR:", e
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(serializers.data)   



"""
    获取指定Project信息
"""
@api_view(['GET', 'POST'])
@permission_classes((AccessPermission,))
@authentication_classes((TokenAuthentication,))
def fetch_project_detail(request):
    print "\n\ndata:"
    print request.data
    
    try:
        project = Project.objects.get(project_id=request.data['params']['project_id'])
    except Exception,e:
        return Response(status=status.HTTP_400_BAD_REQUEST)
   
    if project.owner != request.user and project.creater != request.user:
        print "Forbidden"
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    serializers = ProjectSerializer(project, context={'request': request})
    try:
        print serializers.data
    except Exception,e:
        print "Open ERRPR:", e
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(serializers.data)    
