from datetime import datetime
from rest_framework import serializers
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from payments.models import BankOfAmericaPayment

class CreditCardSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16, validators=[RegexValidator(r'^\d+$')])
    expiration_month = serializers.IntegerField(MinValueValidator(1), MaxValueValidator(12))
    expiration_year = serializers.IntegerField(MinValueValidator(datetime.today().year))
    
class CustomerAddresSerializer(serializers.Serializer):
    direccion = serializers.CharField(max_length=50)
    locacion = serializers.CharField(max_length=50)
    area = serializers.CharField(max_length=50)
    postal = serializers.CharField(max_length=60)
    pais = serializers.CharField(max_length=40)
    telefono = serializers.CharField(max_length=20)

class PaymentDataSerializer(serializers.Serializer):
    total = serializers.DecimalField(max_digits=15, decimal_places=15)
    credit_card = CreditCardSerializer()
    customer_address = CustomerAddresSerializer(required=False)
    ref_id = serializers.CharField(max_length=20, required=False)