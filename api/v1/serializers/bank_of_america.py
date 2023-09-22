from datetime import datetime
from rest_framework import serializers
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator, MaxLengthValidator
from payments.models import BankOfAmericaPayment

class CreditCardSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16, validators=[RegexValidator(r'^\d+$')], required=True)
    expiration_month = serializers.IntegerField(MinValueValidator(1), MaxValueValidator(12), required=True)
    expiration_year = serializers.IntegerField(MinValueValidator(datetime.today().year), required=True)
    
class CustomerAddresSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    address = serializers.CharField(max_length=50, required=True)
    locality = serializers.CharField(max_length=50, required=True)
    area = serializers.CharField(max_length=50, required=True)
    postal = serializers.IntegerField(MaxLengthValidator(5), required=True)
    country = serializers.CharField(max_length=40, required=True)
    email = serializers.CharField(max_length=100, required=True)
    phone = serializers.CharField(max_length=20, required=True)

class PaymentDataSerializer(serializers.Serializer):
    total = serializers.DecimalField(max_digits=15, decimal_places=15)
    credit_card = CreditCardSerializer(required=True)
    customer_address = CustomerAddresSerializer(required=True)