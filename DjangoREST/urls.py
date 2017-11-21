from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from DjangoRESTImage import views
from DjangoRESTImage import projectview
from DjangoRESTImage import imageviews
from DjangoRESTImage import annotationviews

from rest_framework.authtoken import views as authview

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework')),
    url(r'^user/login/', views.login),

    url(r'^user/projects/', projectview.fetch_all_project_list),
    url(r'^user/myprojects/', projectview.fetch_request_user_project_list),
    url(r'^user/projectdetail/',
        projectview.fetch_project_detail),
    
    url(r'^user/images/', imageviews.fetch_all_image_list),
    url(r'^user/projectimages/',
        imageviews.fetch_project_image_list),
    
    url(r'^user/submitannotation/',
        annotationviews.submit_image_annotation),
    url(r'^user/annotationlist/',
        annotationviews.fetch_all_annotation_list),
    url(r'^user/projectimgannotation/',
        annotationviews.fetch_all_images_annotations_list),
    
    url(r'^user/users/', views.user_list),
    url(r'^user/obtaintoken/', authview.obtain_auth_token),
    url(r'^user/init/', views.init_database)
]
