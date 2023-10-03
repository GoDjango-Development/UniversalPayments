from unicodedata import name
from rest_framework import serializers
from django.core.validators import RegexValidator
from payments.models import StripePayment

class StripePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripePayment
        fields = ['transaction_uuid', 'status', 'datetime']   
    
