from rest_framework.permissions import BasePermission
from oauth2_provider.models import AccessToken

class IsAuthenticated(BasePermission):
    
    def has_permission(self, request, view):
        if 'Authorization' not in request.headers:
            return False
        
        authorization = request.headers['Authorization']
        authorization =  authorization.replace('Bearer ', '')
        
        try:
            AccessToken.objects.get(token=authorization)
        except AccessToken.DoesNotExist:
            return False
        
        return bool(request.user and request.user.is_authenticated)