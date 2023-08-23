from rest_framework.permissions import BasePermission
from oauth2_provider.models import Application

class IsValidClient(BasePermission):
    
    def has_permission(self, request, view):
        if 'Clientid' not in request.headers or 'Clientsecret' not in request.headers:
            return False
        
        client_id = request.headers['Clientid']
        client_secret = request.headers['Clientsecret']
        
        try:
            Application.objects.get(client_id=client_id, client_secret=client_secret)
        except Application.DoesNotExist:
            return False
        
        return True