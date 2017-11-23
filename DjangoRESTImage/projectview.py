# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from django.contrib.auth.models import User

from DjangoRESTImage.serializers import *
from DjangoRESTImage.permission import * 
from DjangoRESTImage.authentication import *

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

import json


"""
    获取所有Project信息
"""
@api_view(['GET', 'POST'])
@permission_classes((AccessPermission, AdminPermission,))
@authentication_classes((JSONWebTokenAuthentication,))
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
@authentication_classes((JSONWebTokenAuthentication,))
def fetch_request_user_project_list(request):
    if request.data['type'] == 'ownered':  
        projects = request.user.projects_ownered
    elif request.data['type'] == 'created':
        projects = request.user.projects_created

    serializers = ProjectSerializer(projects, context={'request': request}, many=True)
    try:
        pass
       # print serializers.data
    except Exception,e:
        #print "Open ERRPR:", e
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(serializers.data)   


"""
    获取管理员分配的所有Project信息
"""
@api_view(['GET', 'POST'])
@permission_classes((AccessPermission,))
@authentication_classes((JSONWebTokenAuthentication,))
def fetch_admin_project_list(request):
    
    projects = request.user.projects_created
    serializers = ProjectSerializer(projects, context={'request': request}, many=True)
    try:
        pass
       # print serializers.data
    except Exception,e:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(serializers.data)   



"""
    获取指定Project信息
"""
@api_view(['GET', 'POST'])
@permission_classes((AccessPermission,))
@authentication_classes((JSONWebTokenAuthentication,))
def fetch_project_detail(request):
    
    try:
        project = Project.objects.get(project_id=request.data['params']['project_id'])
    except Exception,e:
        return Response(status=status.HTTP_400_BAD_REQUEST)
   
    if project.owner != request.user and project.creater != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    serializers = ProjectSerializer(project, context={'request': request})
    try:
       pass# print serializers.data
    except Exception,e:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(serializers.data)    
