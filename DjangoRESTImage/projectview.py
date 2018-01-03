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
        project = Project.objects.get(project_id=request.data['project_id'])
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


"""
    管理Project
"""
@api_view(['GET', 'POST'])
@permission_classes((AccessPermission, AdminPermission,))
@authentication_classes((JSONWebTokenAuthentication,))
def manage_project(request):
    rsp = dict()
    # check op
    try:
        op = request.data['op']
    except Exception, e:
        rsp['status'] = 'error'
        rsp['message'] = 'invalid data format'
        return Response(rsp, status=status.HTTP_200_OK)    
    
    if op != 'delete':
        # check data format
        try:    
            # check title 
            title = request.data['title']
            # check creater exist
            creater = User.objects.filter(username=request.data['creater'])
            if len(creater) == 0 or creater[0].userprofile.role != 'admin':
                rsp['status'] = 'error'
                rsp['message'] = 'error creater username'
                return Response(rsp, status=status.HTTP_200_OK)    
            creater = creater[0]
            # check owner
            owner = User.objects.filter(username=request.data['owner'])
            if len(owner) == 0:
                rsp['status'] = 'error'
                rsp['message'] = 'error owner username'
                return Response(rsp, status=status.HTTP_200_OK)    
            owner = owner[0]
            # check images
            images = request.data['images']['images']
            image_objs = list()
            for img_info in images:
                img = Image.objects.filter(title=img_info['title'])
                if len(img) == 0:
                    img = Image(title=img_info['title'],
                            image_src=img_info['image_src'],
                            width=img_info['width'], height=img_info['height'])
                    img.save()
                else:
                    img = img[0]
                image_objs.append(img)
            # check project_type and params 
            project_type = request.data['project_type']
            params = request.data['params'].replace(" ","")
            if  project_type == "tag" or project_type == 'cropper':
                types = params.split(";")
                params = dict()
                params['types'] = types
            else:
                params = json.loads(params)

            if op == 'modify':
                project_id = request.data['project_id']
        except Exception, e:
            rsp['status'] = 'error'
            rsp['message'] = 'invalid data format'
            print e
            return Response(rsp, status=status.HTTP_200_OK)    
    else:
        try:
            project_id = request.data['project_id']
        except Exception, e:
            rsp['status'] = 'error'
            rsp['message'] = 'invalid data format'
            return Response(rsp, status=status.HTTP_200_OK)    



    try:
        if op == "create":
            project = Project(project_type=project_type,
                    creater=creater,
                    owner=owner,
                    params=json.dumps(params),
                    title=title)
            project.save()
            for i,img in enumerate(image_objs):
                project.images.add(img)
                if project_type == "similar":
                    content = params[i]
                    annotation = Annotation(
                        project=project,
                        image=img,
                        content=json.dumps(content),
                        annotation_type=project_type,
                    )
                    annotation.save()

        elif op == "modify":
            project = Project.objects.filter(project_id=project_id)
            if len(project) == 0:
                rsp['status'] = 'error'
                rsp['message'] = 'no such project'
                return Response(rsp, status=status.HTTP_200_OK)    
            project = project[0]
            project.project_type = project_type
            project.creater = creater
            project.owner = owner
            project.params = json.dumps(params)
            project.title = title
            
            for img in project.images.all():
                project.images.remove(img)

            project.save()
            for i,img in enumerate(image_objs):
                project.images.add(img)
                if project_type == "similar":
                    content = params[i]
                    annotation = Annotation.objects.filter(
                        project__project_id=project.project_id,
                        image__image_id=img.image_id
                    )[0]
                    annotation.content = json.dumps(content)
                    annotation.save()

        elif op == "delete":  
            project = Project.objects.filter(project_id=project_id)
            if len(project) == 0:
                rsp['status'] = 'error'
                rsp['message'] = 'no such project'
                return Response(rsp, status=status.HTTP_200_OK)    
            project = project[0]
            project.delete()
    except Exception, e:
        rsp['status'] = 'error'
        rsp['message'] = 'something wrong???'
        print e
        return Response(rsp, status=status.HTTP_200_OK)    

    rsp['status'] = 'success'
    rsp['message'] = 'success'
    return Response(rsp, status=status.HTTP_200_OK)    
