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
                        
        stripe.api_key = API_SECRET_KEY  # Reemplaza con tu clave secreta de Stripe
        
        currency=request.data["currency"]
        data = request.data.copy()
        data['amount']=request.data["amount"]
        data['user'] = request.user.id
        data['transaction_uuid'] = str(uuid.uuid4())
        try:
            card_data = {
                "number": request.data["card_number"],
                "exp_month": request.data["exp_month"],
                "exp_year": request.data["exp_year"],
                "cvc": request.data["cvc"],
            }        

            token = stripe.Token.create(card=card_data)

            if token:
                
                  tokens=token.id
                  charge = stripe.Charge.create(
                      amount=request.data["amount"],
                      currency=currency,
                      source=tokens,
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
                      data['status']="rejected"
                      return Response({'error':'El pago no ha podido realizarse'}, status=500)    
            else:
                
                return Response({'error':'Los Datos de la tarjeta no son correctos'}, status=500)          
        
        except stripe.error.CardError as e:
        
            return Response({"error": e.user_message}, status=500)
     