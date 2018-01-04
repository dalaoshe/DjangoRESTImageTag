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
@permission_classes((AccessPermission, AdminPermission))
@authentication_classes((JSONWebTokenAuthentication,))
def manage_user(request):
    rsp = dict()
    print request.data    
    # check op
    try:
        op = request.data['op']
    except Exception, e:
        rsp['status'] = 'error'
        rsp['message'] = 'invalid data format'
        return Response(rsp, status=status.HTTP_200_OK)    
    
    try:    
        if op != 'delete':
            username = request.data['username'] 
            expire_time = request.data['expiretime']
        if op == 'create':
            password = request.data['password']
        if op != 'create':
            id = request.data['id']
    except Exception, e:
        rsp['status'] = 'error'
        rsp['message'] = 'invalid data format'
        return Response(rsp, status=status.HTTP_200_OK)    



    try:
        if op == "create":
            user = User(username=username)
            user.set_password(password)
            user.save()
            if expire_time != None and expire_time != '':
                user.userprofile.expire_time = expire_time
            user.userprofile.role = "user"
            user.userprofile.save()
        elif op == "modify":
            user = User.objects.filter(id=id)
            if len(user) == 0:
                rsp['status'] = 'error'
                rsp['message'] = 'no such user'
                return Response(rsp, status=status.HTTP_200_OK)    
            user = user[0]
            user.username = username
            user.save()
            user.userprofile.expire_time = expire_time
            user.userprofile.save()

        elif op == "delete":  
            user = User.objects.filter(id=id)
            if len(user) == 0:
                rsp['status'] = 'error'
                rsp['message'] = 'no such user'
                return Response(rsp, status=status.HTTP_200_OK)    
            user = user[0]
            user.delete()
    
    except Exception, e:
        rsp['status'] = 'error'
        rsp['message'] = 'something wrong???'
        print e
        return Response(rsp, status=status.HTTP_200_OK)    

    rsp['status'] = 'success'
    rsp['message'] = 'success'
    return Response(rsp, status=status.HTTP_200_OK)    


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
@permission_classes((AccessPermission, AdminPermission))
@authentication_classes((JSONWebTokenAuthentication,))
def get_detail_user_info_by_id(request):
    rsp = dict() 
    try:
        id = request.data['id']
    except Exception, e:
        rsp['status'] = 'error'
        rsp['message'] = 'invalid data format'
        return Response(rsp, status=status.HTTP_200_OK)    
   
    try:
        user = User.objects.get(id=id)
    except Exception, e:
        rsp['status'] = 'error'
        rsp['message'] = 'no such user'
        return Response(rsp, status=status.HTTP_200_OK)    


    profile = user.userprofile
    res = {
        'id': user.id,
        'username': user.username,
        'role': profile.role,
        'createtime': profile.register_time,
        'expiretime': profile.expire_time,
        'status': 'ok'
    }
    return Response(res, status=status.HTTP_200_OK)    


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

    
    params1 = dict()
    params2 = dict()
    params3 = dict()
    params1['types'] = ['woman', 'dog', 'snack']
    params2 =[
                [
                            {"image_src":"https://img10.360buyimg.com/n5/s500x640_jfs/t7687/164/1418188723/543130/fd1af88e/599ce253N071b3037.png!cc_50x64.jpg",
                                "relation":"0"},
                                    {"image_src":"https://img10.360buyimg.com/n5/s500x640_jfs/t8080/336/277921481/355263/bbdf4bc2/59a51616Nde18895a.jpg!cc_50x64.jpg",
                                        "relation":"1"}
                                        
                                        ],
                    [

                                {"image_src":"https://img10.360buyimg.com/n5/s500x640_jfs/t7687/164/1418188723/543130/fd1af88e/599ce253N071b3037.png!cc_50x64.jpg",
                                    "relation":"1"},
                                        {"image_src":"https://img10.360buyimg.com/n5/s500x640_jfs/t8080/336/277921481/355263/bbdf4bc2/59a51616Nde18895a.jpg!cc_50x64.jpg",
                                            "relation":"1"}

                                            ],
                    [

                                {"image_src":"https://img10.360buyimg.com/n5/s500x640_jfs/t7687/164/1418188723/543130/fd1af88e/599ce253N071b3037.png!cc_50x64.jpg",
                                    "relation":"1"}
                                            ]
             ]
    params3['types'] = ['woman']

    projects1 = Project(project_type='cropper', creater=admin, owner=user,
            params=json.dumps(params1), title='cropper_project')
    projects2 = Project(project_type='similar', creater=admin, owner=user,
            params=json.dumps(params2), title='similar_project')
    projects3 = Project(project_type='tag', creater=admin, owner=user,
            params=json.dumps(params3), title='tag_project')
    if len(Project.objects.filter(title='cropper_project')) == 0:
        projects1.save()
        projects1.images.add(image1)
        projects1.images.add(image2)
        projects1.images.add(image3)
    
    
    init_task('similar_project', 'similar', 
            user, admin, params2, [image1, image2, image3])
    
    
    if len(Project.objects.filter(title='tag_project')) == 0:
        projects3.save()
        projects3.images.add(image1)
        projects3.images.add(image2)

    

    return Response(status=status.HTTP_200_OK)    


def init_task(title, project_type, user, admin, params, images):
    projects = Project.objects.filter(title=title)
    if len(projects) > 0:
        projects[0].delete()
    project = Project(project_type=project_type, creater=admin, owner=user, params=json.dumps(params), title=title)
    project.save()
    for img in images:
        project.images.add(img)
        if project_type == "similar":
            content = [
                {
                    'image_src':'https://img10.360buyimg.com/n5/s500x640_jfs/t7687/164/1418188723/543130/fd1af88e/599ce253N071b3037.png!cc_50x64.jpg',
                  'relation': 0
                  },
                {
                    'image_src':'https://img10.360buyimg.com/n5/s500x640_jfs/t8080/336/277921481/355263/bbdf4bc2/59a51616Nde18895a.jpg!cc_50x64.jpg', 
                   'relation': 1    
                },
                {
                    'image_src':'http://img14.360buyimg.com/n5/s500x640_jfs/t10270/263/1662108454/94989/e9c4a3fb/59e44eabNc1cbd5ef.jpg', 
                    'relation':0
                }
                    ]
            annotation = Annotation(
                project=project,
                image=img,
                content=json.dumps(content),
                annotation_type=project_type,
            )
            annotation.save()


