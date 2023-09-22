import uuid
import json
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from CyberSource import (
    Ptsv2paymentsProcessingInformation, 
    Ptsv2paymentsPaymentInformationCard, 
    Ptsv2paymentsPaymentInformation, 
    Ptsv2paymentsOrderInformationAmountDetails,
    Ptsv2paymentsOrderInformationBillTo,
    Ptsv2paymentsOrderInformation,
    CreatePaymentRequest,
    Ptsv2paymentsClientReferenceInformation,
    PaymentsApi
    
)
from api.permissions import IsAuthenticated
from payments.models import SquaresPayment
from api.v1.serializers import SquarePaymentSerializer
from oauth2_provider.models import AccessToken
from applications.models import BankOfAmericaApplication
from CyberSource.logging.log_configuration import LogConfiguration

class BoAConfiguration:
    def __init__(self):
        self.authentication_type ="http_signature"
        self.merchantid = ""
        self.alternative_merchantid = ""
        # self.run_environment = "apitest.cybersource.com"
        self.run_environment = "api.cybersource.com"
        self.request_json_path = ""
        # JWT PARAMETERS
        self.key_alias = ""
        self.key_pass = ""
        self.key_file_name = ""
        self.alternative_key_alias = ""
        self.alternative_key_pass = ""
        self.alternative_key_file_name = ""
        self.keys_directory = os.path.join(os.getcwd(), "")
        # HTTP PARAMETERS
        self.merchant_keyid = "7a5e137f-7459-4205-9161-bba36a94dfda"
        self.merchant_secretkey = "+wJ+ZYEoQ81MkNinq0pRy3kO3ajZp96vwYkDlf9hQrI="
        self.alternative_merchant_keyid = "7a5e137f-7459-4205-9161-bba36a94dfda"
        self.alternative_merchant_secretkey = "+wJ+ZYEoQ81MkNinq0pRy3kO3ajZp96vwYkDlf9hQrI="
        # META KEY PARAMETERS
        self.use_metakey = False
        self.portfolio_id = ''
        # CONNECTION TIMEOUT PARAMETER
        self.timeout = 1000
        # LOG PARAMETERS
        self.enable_log = True
        self.log_file_name = "cybs"
        self.log_maximum_size = 10487560
        self.log_directory = os.path.join(os.getcwd(), "Logs")
        self.log_level = "Debug"
        self.enable_masking = False
        self.log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self.log_date_format = "%Y-%m-%d %H:%M:%S"
        # PROXY PARAMETERS
        # self.proxy_address = "127.0.0.1"
        # self.proxy_port = "4946"


    # Assigning the configuration properties in the configuration dictionary
    def get_configuration(self):
        configuration_dictionary = ({})
        configuration_dictionary["authentication_type"] = self.authentication_type
        configuration_dictionary["merchantid"] = self.merchantid
        configuration_dictionary["run_environment"] = self.run_environment
        configuration_dictionary["request_json_path"] = self.request_json_path
        configuration_dictionary["key_alias"] = self.key_alias
        configuration_dictionary["key_password"] = self.key_pass
        configuration_dictionary["key_file_name"] = self.key_file_name
        configuration_dictionary["keys_directory"] = self.keys_directory
        configuration_dictionary["merchant_keyid"] = self.merchant_keyid
        configuration_dictionary["merchant_secretkey"] = self.merchant_secretkey
        configuration_dictionary["use_metakey"] = self.use_metakey
        configuration_dictionary["portfolio_id"] = self.portfolio_id
        configuration_dictionary["timeout"] = self.timeout
        log_config = LogConfiguration()
        log_config.set_enable_log(self.enable_log)
        log_config.set_log_directory(self.log_directory)
        log_config.set_log_file_name(self.log_file_name)
        log_config.set_log_maximum_size(self.log_maximum_size)
        log_config.set_log_level(self.log_level)
        log_config.set_enable_masking(self.enable_masking)
        log_config.set_log_format(self.log_format)
        log_config.set_log_date_format(self.log_date_format)
        configuration_dictionary["log_config"] = log_config
        #configuration_dictionary["proxy_address"] = self.proxy_address
        #configuration_dictionary["proxy_port"] = self.proxy_port
        return configuration_dictionary

    def get_alternative_configuration(self):
        configuration_dictionary = ({})
        configuration_dictionary["authentication_type"] = self.authentication_type
        configuration_dictionary["merchantid"] = self.alternative_merchantid
        configuration_dictionary["run_environment"] = self.run_environment
        configuration_dictionary["request_json_path"] = self.request_json_path
        configuration_dictionary["key_alias"] = self.alternative_key_alias
        configuration_dictionary["key_password"] = self.alternative_key_pass
        configuration_dictionary["key_file_name"] = self.alternative_key_file_name
        configuration_dictionary["keys_directory"] = self.keys_directory
        configuration_dictionary["merchant_keyid"] = self.alternative_merchant_keyid
        configuration_dictionary["merchant_secretkey"] = self.alternative_merchant_secretkey
        configuration_dictionary["use_metakey"] = self.use_metakey
        configuration_dictionary["portfolio_id"] = self.portfolio_id
        configuration_dictionary["timeout"] = self.timeout
        log_config = LogConfiguration()
        log_config.set_enable_log(self.enable_log)
        log_config.set_log_directory(self.log_directory)
        log_config.set_log_file_name(self.log_file_name)
        log_config.set_log_maximum_size(self.log_maximum_size)
        log_config.set_log_level(self.log_level)
        log_config.set_enable_masking(self.enable_masking)
        log_config.set_log_format(self.log_format)
        log_config.set_log_date_format(self.log_date_format)
        configuration_dictionary["log_config"] = log_config
        #configuration_dictionary["proxy_address"] = self.proxy_address
        #configuration_dictionary["proxy_port"] = self.proxy_port
        return configuration_dictionary

def del_none(d):
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d

class AllBoAPayments(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        square_payments = SquaresPayment.objects.filter(user=request.user)
        serializer = SquarePaymentSerializer(square_payments, many=True)
        return Response(serializer.data)
    
class BoAPaymentByTransactionUUID(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, idempotency_key):
        try:
            square_payment = SquaresPayment.objects.get(user=request.user, idempotency_key=idempotency_key)
        except SquaresPayment.DoesNotExist:
            return Response(data={'error_details': 'Object not found'}, status=404)
        serializer = SquarePaymentSerializer(square_payment)
        return Response(serializer.data)
    
class CreateBoAPayment(APIView):
    permission_classes = [IsAuthenticated]
   
        
    def post(self, request):
        authorization = request.headers['Authorization'].replace('Bearer ', '')
        try:
            application = BankOfAmericaApplication.objects.get(pk=AccessToken.objects.get(token=authorization).application.pk)
        except BankOfAmericaApplication.DoesNotExist:
            return Response(data={'error_details': 'Authorization token is not from Square Application'}, status=400)
        
        user = application.user
        data = request.data
        
        # for security no payment info is stored on the system
        processingInformationCapture = False

        processingInformation = Ptsv2paymentsProcessingInformation(
            capture=processingInformationCapture
        )

        # build card info
        creditCardData = data.get('credit_card')
        paymentInformationCardNumber = creditCardData.get('card_number')
        paymentInformationCardExpirationMonth = creditCardData.get('expiration_month')
        paymentInformationCardExpirationYear = creditCardData.get('expiration_year')
        paymentInformationCard = Ptsv2paymentsPaymentInformationCard(
            number=paymentInformationCardNumber,
            expiration_month=paymentInformationCardExpirationMonth,
            expiration_year=paymentInformationCardExpirationYear
        )

        paymentInformation = Ptsv2paymentsPaymentInformation(
            card=paymentInformationCard.__dict__
        )

        # build money attrs
        orderInformationAmountDetailsTotalAmount = data.get('total')
        orderInformationAmountDetailsCurrency = "USD"
        orderInformationAmountDetails = Ptsv2paymentsOrderInformationAmountDetails(
            total_amount=orderInformationAmountDetailsTotalAmount,
            currency=orderInformationAmountDetailsCurrency
        )
        

        # build payer data
        customerAddressData = data.get('customer_address')
        orderInformationBillToFirstName = customerAddressData.get('first_name')
        orderInformationBillToLastName = customerAddressData.get('last_name')
        # orderInformationBillToAddress1 = user.direccion
        orderInformationBillToAddress1 = customerAddressData.get('address')
        # orderInformationBillToLocality = user.ciudad
        orderInformationBillToLocality = customerAddressData.get('locality')
        orderInformationBillToAdministrativeArea = customerAddressData.get('area')
        # orderInformationBillToPostalCode = user.codigo_postal or "33166"
        orderInformationBillToPostalCode = customerAddressData.get('postal')
        orderInformationBillToCountry = customerAddressData.get('country')
        orderInformationBillToEmail = customerAddressData.get('email')
        orderInformationBillToPhoneNumber = customerAddressData.get('phone')
        orderInformationBillTo = Ptsv2paymentsOrderInformationBillTo(
            first_name=orderInformationBillToFirstName,
            last_name=orderInformationBillToLastName,
            address1=orderInformationBillToAddress1,
            locality=orderInformationBillToLocality,
            administrative_area=orderInformationBillToAdministrativeArea,
            postal_code=orderInformationBillToPostalCode,
            country=orderInformationBillToCountry,
            email=orderInformationBillToEmail,
            phone_number=orderInformationBillToPhoneNumber
        )
        orderInformation = Ptsv2paymentsOrderInformation(
            amount_details=orderInformationAmountDetails.__dict__,
            bill_to=orderInformationBillTo.__dict__,
        )

        # make the order
        # create a random string
        cric = uuid.uuid4().hex[:6].upper()
        
        clientReferenceInformationCode = "TC{}".format(cric)
        clientReferenceInformation = Ptsv2paymentsClientReferenceInformation(
            code=clientReferenceInformationCode
        )
        requestObj = CreatePaymentRequest(
            client_reference_information=clientReferenceInformation.__dict__,
            processing_information=processingInformation.__dict__,
            payment_information=paymentInformation.__dict__,
            order_information=orderInformation.__dict__
        )

        # delete empty fields
        requestObj = del_none(requestObj.__dict__)
        requestObj = json.dumps(requestObj)
        try:
            # get the gateway specifications
            config_obj = BoAConfiguration()
            config_obj.merchantid = application.merchant_id
            config_obj.alternative_merchantid = application.merchant_id
            config_obj.run_environment = application.run_environment
            config_obj.merchant_keyid = application.key
            config_obj.merchant_secretkey = application.shared_secret_key
            client_config = config_obj.get_configuration()
            # attempt to make the transaction
            api_instance = PaymentsApi(client_config)
            # get the response
            return_data, status, body = api_instance.create_payment(requestObj)
            # order.status = str(status)
            # order.destinatario = order.destinatario + str(return_data) + ' '
            # order.destinatario = order.destinatario + str(status) + ' '
            # order.destinatario = order.destinatario + str(body) + ' '
            # order.save()
            if status != '401':
                return Response(data={"status": "success"}, content_type='application/json', status=201)
            else:
                return Response(data={"status": "error_payment"}, content_type='application/json', status=400)
            # return the response
        except Exception as e:
            print(e)
            return Response(data={"status": "error_gateway"}, content_type='application/json', status=500)