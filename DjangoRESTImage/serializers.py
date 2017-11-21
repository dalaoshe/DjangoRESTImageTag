from django.contrib.auth.models import User, Group
from rest_framework import serializers
from models import *

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name')

class UserSerializer(serializers.ModelSerializer):
    projects_ownered = serializers.PrimaryKeyRelatedField(many=True,
            queryset=Project.objects.all())
    
    projects_created = serializers.PrimaryKeyRelatedField(many=True,
            queryset=Project.objects.all())
    
    class Meta:
        model = User
        write_only=False
        fields = ('id','is_active', 'password', 'username', 'email', 'groups',
                'projects_created', 'projects_ownered')

class ImageSerializer(serializers.ModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(many=True,
            queryset=Project.objects.all())
    class Meta:
        model = Image
        fields = ('image_id', 'image_src', 'width', 'height', 'projects',)


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    creater = serializers.ReadOnlyField(source='creater.username')
    images = ImageSerializer('images', many=True, read_only=True)
    class Meta:
        model = Project
        fields = ('project_id', 'title', 'project_type', 'owner', 'creater', 'images', 'params')


class AnnotationSerializer(serializers.ModelSerializer):
    image = serializers.ReadOnlyField(source='image.image_id')
    project = serializers.ReadOnlyField(source='project.project_id')
    class Meta:
        model = Annotation
        fields = ('annotation_id', 'project', 'image','content')
