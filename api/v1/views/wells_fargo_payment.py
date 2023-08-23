from rest_framework.views import APIView
from rest_framework.response import Response
from api.permissions import IsAuthenticated
from api.v1.utils.wells_fargo import *
from payments.models import WellsFargoPayment
from api.v1.serializers.wells_fargo import TransactionDetailsSerializer, WellsFargoPaymentSerializer
from oauth2_provider.models import AccessToken
from django.utils import timezone
from applications.models import WellsFargoApplication
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import createTransactionController, getTransactionDetailsController


class AllWFPayments(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        wf_payments = WellsFargoPayment.objects.filter(user=request.user)
        serializer = WellsFargoPaymentSerializer(wf_payments, many=True)
        return Response(serializer.data)
    
class WFPaymentByTransactionUUID(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, transaction_uuid):
        authorization = request.headers['Authorization'].replace('Bearer ', '')
        try:
            application = WellsFargoApplication.objects.get(pk=AccessToken.objects.get(token=authorization).application.pk)
            wf_payment = WellsFargoPayment.objects.get(user=request.user, transaction_uuid=transaction_uuid)
        except WellsFargoApplication.DoesNotExist:
            return Response(data={'error_details': 'Authorization token is not from Wells Fargo Application'}, status=403)
        except WellsFargoPayment.DoesNotExist:
            return Response(data={'error_details': 'Object not found'}, status=404)
            
        """
        Get transaction details
        """
        
        data = request.data
        
        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = application.api_id
        merchantAuth.transactionKey = application.api_secret
        
        transactionDetailsRequest = apicontractsv1.getTransactionDetailsRequest()
        transactionDetailsRequest.merchantAuthentication = merchantAuth
        transactionDetailsRequest.transId = transaction_uuid
        
        transactionDetailsController = getTransactionDetailsController(transactionDetailsRequest)
        transactionDetailsController.execute()
        transactionDetailsResponse = transactionDetailsController.getresponse()
        
        if transactionDetailsResponse is not None:
            if transactionDetailsResponse.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
                transaction = transactionDetailsResponse.transaction
                try:
                    transaction_data = build_transaction_data(transaction)
                except ValueError as error:
                    return Response(error.args[0], 500)
                transaction_details_serializer = TransactionDetailsSerializer(data=transaction_data)
                if transaction_details_serializer.is_valid():
                    return Response({"transaction": transaction_details_serializer.data}, 200)
                return Response({"errors": transaction_details_serializer.errors}, 500)
            else:
                return Response({"error_details": f"{transactionDetailsResponse.messages.message[0]['text'].text}"}, 400)
        else:
            if transactionDetailsResponse.messages is not None:
                return Response({"error_details": f"{transactionDetailsResponse.messages.message[0]['text'].text}"}, 400)
    
class CreateWFPayment(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        authorization = request.headers['Authorization'].replace('Bearer ', '')
        try:
            application = WellsFargoApplication.objects.get(pk=AccessToken.objects.get(token=authorization).application.pk)
        except WellsFargoApplication.DoesNotExist:
            return Response(data={'error_details': 'Authorization token is not from Wells Fargo Application'}, status=400)
        
        """
        Charge a credit card
        """
        data = request.data
        
        try:
            apiLoginId = application.api_id
            transactionKey = application.api_secret
        except Exception as error:
            return Response({"error: Credenciales de Wells Fargo incorrectas. Obtenga su llave e intente de nuevo."}, 500)
        # transactionId = data.get('transactionId') #"60163892435"
        # payerId = data.get('payerId') #"LM6NCLZ5RAKBY"
        # customerProfileId = data.get('customerProfileId') #"1929820324"
        # customerPaymentProfileId = data.get('customerPaymentProfileId') #"1841987457"
        # customerProfileShippingId = data.get('customerProfileShippingId') #"901056173"
        amount = data.get('amount') #"12.23"
        # subscriptionId = data.get('subscriptionId') #"326280"
        # days = 34

        """
        Charge a credit card
        """
        # Create a merchantAuthenticationType object with authentication details
        # retrieved from the constants file
        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = apiLoginId
        merchantAuth.transactionKey = transactionKey

        # Create the payment data for a credit card
        try:
            creditCard = create_credit_card(data)
        except ValueError as error:
            return Response(error.args[0], 500)

        # Add the payment data to a paymentType object
        payment = apicontractsv1.paymentType()
        payment.creditCard = creditCard

        # Create order information
        try:
            order = create_order(data)
        except ValueError as error:
            return Response(error.args[0], 500)
            
        # Set the customer's Bill To address
        try:
            customerAddress = create_customer_address(data)
        except ValueError as error:
            return Response(error.args[0], 500)
            
        # Set the customer's identifying information
        try:
            customerData = create_customer_data(data)
        except ValueError as error:
            return Response(error.args[0], 500)

        # Add values for transaction settings
        try:
            settings = create_settings(data)
        except ValueError as error:
            return Response(error.args[0], 500)

        # build the array of line items
        try:
            lineItems = create_line_items(data)
        except ValueError as error:
            return Response(error.args[0], 500)

        # Create a transactionRequestType object and add the previous objects to it.
        transactionrequest = apicontractsv1.transactionRequestType()
        transactionrequest.transactionType = "authCaptureTransaction"
        transactionrequest.amount = amount
        transactionrequest.payment = payment
        transactionrequest.order = order
        transactionrequest.billTo = customerAddress
        transactionrequest.customer = customerData
        transactionrequest.transactionSettings = settings
        transactionrequest.lineItems = lineItems

        # Assemble the complete transaction request
        createtransactionrequest = apicontractsv1.createTransactionRequest()
        createtransactionrequest.merchantAuthentication = merchantAuth
        createtransactionrequest.refId = data.get('refId')
        createtransactionrequest.transactionRequest = transactionrequest
        # Create the controller
        createtransactioncontroller = createTransactionController(
            createtransactionrequest)
        createtransactioncontroller.execute()

        response = createtransactioncontroller.getresponse()

        if response is not None:
            # Check to see if the API request was successfully received and acted upon
            if response.messages.resultCode == "Ok":
                # Since the API request was successful, look for a transaction response
                # and parse it to display the results of authorizing the card
                if hasattr(response.transactionResponse, 'messages') is True:
                    data = request.data.copy()
                    data['transaction_uuid'] = f"{response.transactionResponse.transId}"
                    data['datetime'] = timezone.now()
                    print(data)
                    
                    serializer = WellsFargoPaymentSerializer(data=data)
                    if serializer.is_valid():
                        print(serializer.validated_data)
                        wf_payment = serializer.save()
                        wf_payment.wells_fargo_app = application
                        wf_payment.user = request.user
                        wf_payment.status = 'completed'
                        wf_payment.save()
                        return Response(serializer.data, status=201)
                    return Response({
                            "error_details": "Bad request",
                            "errors": f"{serializer.errors}"
                        }, status=400)
                else:
                    print('Failed Transaction.')
                    if hasattr(response.transactionResponse, 'errors') is True:
                        return Response({"error_details": f"{response.transactionResponse.errors.error[0].errorText}"}, status=400)
            # Or, print errors if the API request wasn't successful
            else:
                print('Failed Transaction.')
                if hasattr(response, 'transactionResponse') is True and hasattr(
                        response.transactionResponse, 'errors') is True:
                    return Response({"error_details": f"{response.transactionResponse.errors.error[0].errorText}"}, status=400)
                else:
                    return Response({"error_details": f"{response.transactionResponse.errors.error[0].errorText}"}, status=400)
        else:
            return Response(f"result: Connection timeout", status=408)
        