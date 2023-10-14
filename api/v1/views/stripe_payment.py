import uuid
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from api.permissions import IsValidClient, IsAuthenticated
from payments.models import StripePayment
from api.v1.serializers import StripePaymentSerializer
from oauth2_provider.models import AccessToken
from applications.models import StripeApplication

class AllStripePayments(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        stripe_payments = StripePayment.objects.filter(user=request.user)
        serializer = StripePaymentSerializer(stripe_payments, many=True)
        return Response(serializer.data)
    
class StripePaymentByTransactionUUID(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, transaction_uuid):
        try:
            stripe_payment = StripePayment.objects.get(user=request.user, transaction_uuid=transaction_uuid)
        except StripePayment.DoesNotExist:
            return Response(data={'error_details': 'Object not found'}, status=404)
        serializer = StripePaymentSerializer(stripe_payment)
        return Response(serializer.data)
    
class CreateStripePayment(APIView):
    permission_classes = [IsAuthenticated]   
        
    def post(self, request):
        authorization = request.headers['Authorization'].replace('Bearer ', '')
        try:
            application = StripeApplication.objects.get(pk=AccessToken.objects.get(token=authorization).application.pk)
        except StripeApplication.DoesNotExist:
            return Response(data={'error_details': 'Authorization token is not from Stripe Application'}, status=400)
        
        API_PUBLIC_KEY=application.api_public_key
        API_SECRET_KEY=application.api_secret_key       
                        
        stripe.api_key = API_SECRET_KEY  
        
        currency=request.data["currency"]
        data = request.data.copy()
        data['amount']=request.data["amount"]
        data['user'] = request.user.id
        data['transaction_uuid'] = str(uuid.uuid4())
        token = request.data["token"]
        try: 
            
            if token:
                  charge = stripe.Charge.create(
                      amount=float(request.data["amount"])*100,
                      currency=currency,
                      source=token,
                      )
                  if charge.status == "succeeded":
                        data['status']=charge.status
                        serializer = StripePaymentSerializer(data=data)
                        if serializer.is_valid():
                           print(serializer.validated_data)
                           serializer.save()
                           return Response(serializer.data, status=201)
                        return Response(serializer.errors, status=400)
                  else:
                      try:
                           cargo = stripe.Charge.retrieve(charge.id)
                           data['status']="rejected"
                           cargo.refund()
                           return Response({'error':'El pago no ha podido realizarse'}, status=500) 
                           
                           
                      except stripe.error.StripeError as e:
       
                           return Response({'error':'El pago no ha podido ser cancelado'}, status=500) 
                         
            else:
                
                return Response({'error':'Los Datos de la tarjeta no son correctos'}, status=500)          
        
        except stripe.error.CardError as e:
        
            return Response({"error": e.user_message}, status=500)
     