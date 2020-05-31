from .models import *

def isProfileCreated(function):
    def check(request,*args,**kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
            print(profile)
            return function(request)
        except:
            profile = Profile(user=request.user)
            profile.save()
            print(profile)
            return function(request)
    
    return check
        