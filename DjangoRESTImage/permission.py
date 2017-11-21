from rest_framework import permissions


class AccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        print "User:", request.user
        print "Auth:", request.auth
        print "request", request
        if request.auth != None:
            return True 
        else:
            #pass
            return False

