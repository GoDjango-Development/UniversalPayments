from rest_framework import serializers
from oauth2_provider.models import AccessToken, RefreshToken

class AccesTokenSerializer(serializers.ModelSerializer):
    token_type = serializers.CharField(default='Bearer')
    
    class Meta:
        model = AccessToken
        fields = ['token', 'token_type', 'expires',]