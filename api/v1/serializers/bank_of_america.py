from datetime import datetime
from rest_framework import serializers
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator, MaxLengthValidator
from payments.models import BankOfAmericaPayment

class CreditCardSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16, validators=[RegexValidator(r'^\d+$')])
    expiration_month = serializers.IntegerField(MinValueValidator(1), MaxValueValidator(12))
    expiration_year = serializers.IntegerField(MinValueValidator(datetime.today().year))
    
class CustomerAddresSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    address = serializers.CharField(max_length=50)
    locality = serializers.CharField(max_length=50)
    area = serializers.CharField(max_length=50)
    postal = serializers.IntegerField(MaxLengthValidator(5))
    country = serializers.CharField(max_length=40)
    email = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20)

class PaymentDataSerializer(serializers.Serializer):
    total = serializers.DecimalField(max_digits=15, decimal_places=15)
    credit_card = CreditCardSerializer()
    customer_address = CustomerAddresSerializer(required=True)