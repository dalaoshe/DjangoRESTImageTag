# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes


from DjangoRESTImage.serializers import *
from django.contrib.auth.models import User

from DjangoRESTImage.permission import * 
from DjangoRESTImage.authentication import *
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

import json,datetime

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or
    edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer



@api_view(['GET', 'POST'])
@permission_classes((AccessPermission, AdminPermission))
@authentication_classes((JSONWebTokenAuthentication,))
def user_list(request):

    users = User.objects.all()
    serializers = UserSerializer(users, context={'request': request}, many=True)
    try:
        pass
    except Exception,e:
        pass
    return Response(serializers.data)    


@api_view(['GET', 'POST'])
@permission_classes((AccessPermission,))
@authentication_classes((JSONWebTokenAuthentication,))
def detail_user_info(request):
    user = request.user
    profile = request.user.userprofile
    res = {
        'name': user.username,
        'role': profile.role,
        'status': 'ok',
        'notifyCount': 12,
            }
    return Response(res)    


@api_view(['GET', 'POST'])
def init_database(request):
    user = User.objects.filter(username='dalaoshe')
    if len(user) == 0:
        user = User(username='dalaoshe', password='clyb0515')
        user.set_password('clyb0515')
        user.save()
    else: 
        user = user[0]

    admin = User.objects.filter(username='admin') 
    if len(admin) == 0:
        admin = User(username='admin', password='dalaoshe')
        admin.set_password('dalaoshe')
        admin.save()
    else:
        admin = admin[0]
    
    delta = datetime.timedelta(days=10000)
    expire = delta + datetime.datetime.now()
    admin.userprofile.expire_time = expire 
    admin.userprofile.role = "admin"
    admin.userprofile.save()

    image1 =  Image.objects.filter(title='image1')
    if len(image1) == 0:
        print "New Image1"
        image1 = Image(title='image1', 
                image_src='http://img14.360buyimg.com/n5/s500x640_jfs/t10270/263/1662108454/94989/e9c4a3fb/59e44eabNc1cbd5ef.jpg', 
                width=128,
            height=256)
        image1.save()
    else: 
        image1 = image1[0]

    image2 = Image.objects.filter(title='image2') 
    if len(image2) == 0:
        print "New Image2"
        image2 = Image(title='image2', 
                image_src='https://img10.360buyimg.com/n5/s500x640_jfs/t8080/336/277921481/355263/bbdf4bc2/59a51616Nde18895a.jpg!cc_50x64.jpg', 
                width=128,
            height=256)
        image2.save()
    else:
        image2 = image2[0]


    image3 =  Image.objects.filter(title='image3')
    if len(image3) == 0:
        print "New Image3"
        image3 = Image(title='image3', 
                image_src='https://img10.360buyimg.com/n5/s500x640_jfs/t7687/164/1418188723/543130/fd1af88e/599ce253N071b3037.png!cc_50x64.jpg',
                width=128,
            height=256)
        image3.save()
    else: 
        image3 = image3[0]

    
    params = dict()
    params['types'] = ['woman', 'dog', 'snack']

    projects1 = Project(project_type='cropper', creater=admin, owner=user,
            params=json.dumps(params), title='cropper_project')
    projects2 = Project(project_type='similar', creater=admin, owner=user,
            params=json.dumps(params), title='similar_project')
    projects1.save()
    projects2.save()
    projects1.images.add(image1)
    projects1.images.add(image2)
    projects1.images.add(image3)
    projects2.images.add(image1)
    projects2.images.add(image2)
    projects2.images.add(image3)

    

    return Response(status=status.HTTP_200_OK)    

