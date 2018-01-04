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
    获取所有指定project-image对的annotation信息
"""
@api_view(['GET', 'POST'])
@permission_classes((AccessPermission,))
@authentication_classes((JSONWebTokenAuthentication,))
def fetch_all_images_annotations_list(request):
    datas = request.data
    project_ids = datas['project_ids']
    image_ids = datas['image_ids']
    annotation_type = datas['annotation_type']
    annotations = list()
    for project_id, image_id in zip(project_ids, image_ids):
        try:
            annotation = Annotation.objects.get(
                 project__project_id=project_id,
                 image__image_id=image_id
              )
        except Exception,e:
            print e
            annotation = None
        annotations.append(annotation)

    serializers = AnnotationSerializer(annotations, context={'request': request}, many=True)
    try:
        pass
        #print serializers.data
    except Exception,e:
        pass
        #print "Open ERRPR:", e
    
    return Response(serializers.data, status=status.HTTP_200_OK)    

"""
    提交annotation
"""
@api_view(['GET', 'POST'])
@permission_classes((AccessPermission,))
@authentication_classes((JSONWebTokenAuthentication,))
def submit_image_annotation(request):
    datas = request.data
    project_id = datas['project_id']
    image_id = datas['image_id']
    annotation_type = datas['annotation_type']

    annotation = Annotation.objects.filter(
            project__project_id=project_id,
            image__image_id=image_id
            )
    if len(annotation) == 0:
        try:
            image = Image.objects.get(image_id=image_id)
            project = Project.objects.get(project_id=project_id)
        except Exception,e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        #print 'new one'
        annotation = Annotation(
            project=project,
            image=image,
            content=json.dumps(datas['content']),
            annotation_type=annotation_type,
                )
        annotation.save()
    else:
        #print 'update'
        annotation = annotation[0]
        annotation.content = json.dumps(datas['content'])
        annotation.save()

    return Response({'status': 'ok'},status=status.HTTP_200_OK)    


"""
    获取所有annotation信息
"""
@api_view(['GET', 'POST'])
@permission_classes((AccessPermission, AdminPermission))
@authentication_classes((JSONWebTokenAuthentication,))
def fetch_all_annotation_list(request):
    
    annotations = Annotation.objects.all()
    serializers = AnnotationSerializer(annotations, context={'request': request}, many=True)
    try:
        pass
    except Exception,e:
        pass #print "Open ERRPR:", e
    return Response(serializers.data)    

