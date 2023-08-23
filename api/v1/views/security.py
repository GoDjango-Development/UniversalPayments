from django.http import HttpResponseBadRequest, HttpResponseForbidden
from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.models import AccessToken, RefreshToken
from oauth2_provider.settings import oauth2_settings
from api.permissions.is_valid_client import IsValidClient
from api.v1.serializers.security import AccesTokenSerializer
from misc.models import Application
from django.utils import timezone
from django.utils.timezone import now
from datetime import timedelta

class LoginView(APIView):
    authentication_classes = []
    permission_classes = [IsValidClient]
    
    def post(self, request, *args, **kwargs):
        client_id = request.headers['Clientid']
        client_secret = request.headers['Clientsecret']
            
        application = Application.objects.get(client_id=client_id, client_secret=client_secret)
        
        user = application.user
        user.last_login = now()
        user.save()
        
        from oauthlib import common
        expires = timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
        access_token = AccessToken(
            user=user,
            scope='read write',
            expires=expires,
            token=common.generate_token(),
            application=application
        )
        access_token.save()
        print(access_token)
        
        refresh_token = RefreshToken(
            user=user,
            token=common.generate_token(),
            application=application,
            access_token=access_token
        )
        refresh_token.save()
        
        serializer = AccesTokenSerializer(access_token)

        return Response(serializer.data)