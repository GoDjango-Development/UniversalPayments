from rest_framework import serializers
from payments.models import SquaresPayment

class SquarePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SquaresPayment
        fields = ['user', 'square_app', 'idempotency_key', 'status', 'datetime','source_id','customer_id','amount','currency']
        
        
    def to_representation(self,instance):
            return{
            'id':instance.id,
            'user':instance.user.id,
            'square_app':instance.square_app,
            'idempotency_key':instance.idempotency_key,
            'source_id':instance.source_id,
            "amount_money":{
                'amount':instance.amount,
                'currency':instance.currency
            },
            'customer_id':instance.customer_id,
            'status':instance.status,
            'datetime':instance.datetime
            }