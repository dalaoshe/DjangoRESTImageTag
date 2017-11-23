from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions


import datetime

def jwt_response_payload_handler(token, user=None, request=None):
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=900)
    #now = now + delta
    profile = user.userprofile
    print "now:" ,now
    has_expire = now > profile.expire_time.replace(tzinfo=None)
    
    if has_expire:
        print "expire account:", user , " delete"
        return {
            'expire': True,
            'status': 'error',
            'message': 'expire account',
                } 
    return {
        'token': token,
        'role': profile.role,
        'status': 'ok',
    }


def jwt_payload_handler(user):
    #print user
    payload = {
        'username': user.username,
        'user_id': user.pk,
        'role': user.userprofile.role
    }
    return payload



