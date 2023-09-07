import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from square.client import Client
from api.permissions import IsValidClient, IsAuthenticated
from payments.models import SquaresPayment
from api.v1.serializers import SquarePaymentSerializer
from oauth2_provider.models import AccessToken
from applications.models import SquaresApplication


class AllSquarePayments(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        square_payments = SquaresPayment.objects.filter(user=request.user)
        serializer = SquarePaymentSerializer(square_payments, many=True)
        return Response(serializer.data)
    
class SquarePaymentByTransactionUUID(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, idempotency_key):
        try:
            square_payment = SquaresPayment.objects.get(user=request.user, idempotency_key=idempotency_key)
        except SquaresPayment.DoesNotExist:
            return Response(data={'error_details': 'Object not found'}, status=404)
        serializer = SquarePaymentSerializer(square_payment)
        return Response(serializer.data)
    
class CreateSquarePayment(APIView):
    permission_classes = [IsAuthenticated]
   
        
    def post(self, request):
        authorization = request.headers['Authorization'].replace('Bearer ', '')
        try:
            application = SquaresApplication.objects.get(pk=AccessToken.objects.get(token=authorization).application.pk)
        except SquaresApplication.DoesNotExist:
            return Response(data={'error_details': 'Authorization token is not from Square Application'}, status=400)
        
        ACCESS_TOKEN=application.access_token
        APPLICATION_ID =application.application_id 
        LOCATION_ID =application.location_id
        ENVIROMENT=application.environment 
        
        client = Client(
        access_token=ACCESS_TOKEN,
        environment=ENVIROMENT)
       
        
        location = client.locations.retrieve_location(location_id=LOCATION_ID).body["location"]
        ACCOUNT_CURRENCY = location["currency"]
        ACCOUNT_COUNTRY = location["country"]
        
        data = request.data.copy()
        
      
        data['user'] = request.user.id
        data['idempotency_key'] = str(uuid.uuid4())
        data['currency'] = ACCOUNT_CURRENCY
        data['reference_id'] = str(uuid.uuid4())
       
        request_body={
       "source_id":  request.data['source_id'],
       "amount_money":{
           "amount": float(request.data['amount'])*100,
           "currency": data['currency']
       },
    
       "idempotency_key": data['idempotency_key'],
       "autocomplete": True,
       "customer_id": request.data['customer_id'],
       "reference_id": data['reference_id']
      }
        pagos=client.payments
        response=pagos.create_payment(request_body)
        if response.is_success():
            payment = response.body['payment']
            estado = payment['status']
            if estado == 'COMPLETED':
              # Acciones para un pago completado exitosamente
                 data['status']=estado.lower()
            elif estado == 'FAILED':
              # Acciones para un pago fallido
                 data['status']="rejected"
            else:
              # Acciones para otros estados de pago                   
                 data['status']="pending"
                 
            serializer = SquarePaymentSerializer(data=data)
            if serializer.is_valid():
                print(serializer.validated_data)
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        else:
            return Response({'error':'El pago no ha podido realizarse'}, status=500)