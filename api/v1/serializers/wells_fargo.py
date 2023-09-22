from rest_framework import serializers
from django.core.validators import RegexValidator
from payments.models import WellsFargoPayment

class WellsFargoPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WellsFargoPayment
        fields = ['transaction_uuid', 'status', 'datetime']
        
class TransactionFDSFilterSerializer(serializers.Serializer):
    name = serializers.CharField()
    action = serializers.CharField()

class TransactionOrderSerializer(serializers.Serializer):
    invoiceNumber = serializers.CharField()
    description = serializers.CharField()
    purchaseOrderNumber = serializers.CharField()
    
class TransactionTaxSerializer(serializers.Serializer):
    amount = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    
class TransactionLineItemSerializer(serializers.Serializer):
    itemId = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    quantity = serializers.CharField()
    unitPrice = serializers.CharField()
    taxable = serializers.BooleanField()
    
class TransactionCreditCardSerializer(serializers.Serializer):
    cardNumber = serializers.CharField()
    expirationDate = serializers.CharField()
    cardType = serializers.CharField()
    
class TransactionPaymentSerializer(serializers.Serializer):
    creditCard = TransactionCreditCardSerializer()
    
class TransactionCustomerSerializer(serializers.Serializer):
    type = serializers.CharField()
    id = serializers.CharField()
    email = serializers.EmailField()
    
class TransactionCustomerAddressSerializer(serializers.Serializer):
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    company = serializers.CharField()
    address = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    zip = serializers.CharField()
    country = serializers.CharField()
    phoneNumber = serializers.CharField()
    faxNumber = serializers.CharField()

class TransactionDetailsSerializer(serializers.Serializer):
    transId = serializers.CharField()
    submitTimeUTC = serializers.CharField()
    submitTimeLocal = serializers.CharField()
    transactionType = serializers.CharField()
    transactionStatus = serializers.CharField()
    responseCode = serializers.CharField()
    responseReasonCode = serializers.CharField()
    responseReasonDescription = serializers.CharField()
    authCode = serializers.CharField()
    AVSResponse = serializers.CharField()
    cardCodeResponse = serializers.CharField()
    FDSFilters = TransactionFDSFilterSerializer(required=False, many=True)
    order = TransactionOrderSerializer(required=False)
    authAmount = serializers.CharField()
    settleAmount = serializers.CharField()
    tax = TransactionTaxSerializer(required=False)
    lineItems = TransactionLineItemSerializer(required=False, many=True)
    taxExempt = serializers.CharField()
    payment = TransactionPaymentSerializer()
    customer = TransactionCustomerSerializer(required=False)
    customerAddress = TransactionCustomerAddressSerializer(required=False)
    
class WellsFargoPaymentDetailsSerializer(serializers.Serializer):
    transaction = TransactionDetailsSerializer()

# INPUT DATA
class CreditCardSerializer(serializers.Serializer):
    cardNumber = serializers.CharField(max_length=16, validators=[RegexValidator(r'^\d+$')])
    expirationDate = serializers.DateField(format='%Y-%m', input_formats=['%Y-%m'])
    cardCode = serializers.CharField(max_length=4, validators=[RegexValidator(r'^\d+$')])
    
class OrderSerializer(serializers.Serializer):
    invoiceNumber = serializers.CharField(max_length=20)
    description = serializers.CharField(max_length=255)

class CustomerAddressSerializer(serializers.Serializer):
    firstName = serializers.CharField(max_length=50)
    lastName = serializers.CharField(max_length=50)
    company = serializers.CharField(max_length=50)
    address = serializers.CharField(max_length=60)
    city = serializers.CharField(max_length=40)
    state = serializers.CharField(max_length=40)
    zip = serializers.CharField(max_length=20)
    country = serializers.CharField(max_length=20)
    phoneNumber = serializers.CharField(max_length=25)
    faxNumber = serializers.CharField(max_length=25)
        
class CustomerDataSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=['individual', 'business'])
    id = serializers.CharField(validators=[RegexValidator(r'^[0-9a-zA-Z]+$')])
    email = serializers.EmailField()
    
setting_names = {
    'allowPartialAuth',
    'duplicateWindow',
    'emailCustomer',
    'headerEmailReceipt',
    'footerEmailReceipt',
    'recurringBilling'
}    
    
class SettingSerializer(serializers.Serializer):
    settingName = serializers.ChoiceField(choices=setting_names)
    settingValue = serializers.CharField()
    
class ItemSerializer(serializers.Serializer):
    itemId = serializers.CharField(max_length=31)
    name = serializers.CharField(max_length=31)
    description = serializers.CharField(max_length=255)
    quantity = serializers.DecimalField(max_digits=10, decimal_places=4)
    unitPrice = serializers.DecimalField(max_digits=10, decimal_places=4)
    taxable = serializers.BooleanField(required=False)

class PaymentDataSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=15, decimal_places=15)
    creditCard = CreditCardSerializer()
    order = OrderSerializer(required=False)
    lineItems = ItemSerializer(many=True, required=False)
    customerAddress = CustomerAddressSerializer(required=False)
    customerData = CustomerDataSerializer(required=False)
    settings = SettingSerializer(many=True, required=False)
    refId = serializers.CharField(max_length=20, required=False)