from rest_framework import permissions
from rest_framework_jwt.settings import api_settings
import datetime

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
class AccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        payload = jwt_decode_handler(request.auth)
        now = datetime.datetime.now()
        profile = request.user.userprofile

        if request.user.is_anonymous():
            return False
        else:
            print "User:", request.user
            print "Auth:", request.auth
            print "Request", request
            print "Payload:", payload
            print "Profile Register:",profile.register_time
            print "Profile Expire:",profile.expire_time
            print "Now:" ,now
            print "Priviledge:",payload['role']

            r1 = now > profile.register_time.replace(tzinfo=None)
            has_expire = now > profile.expire_time.replace(tzinfo=None)
            if has_expire:
                print "expire account:", request.user , " delete"
                request.user.delete()
                return False
            
            print "Expire Register:",r1," Expired:", has_expire
            
            return True


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        payload = jwt_decode_handler(request.auth)
        if payload['role'] != "admin":
            return False
        return True

