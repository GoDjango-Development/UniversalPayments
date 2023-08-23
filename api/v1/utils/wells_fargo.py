
from api.v1.serializers.wells_fargo import *
from authorizenet import apicontractsv1

# !!!!!!!!GET TRANSACTION DETAILS!!!!!!!!! #

def get_fdsfilters_data(transaction):
    if hasattr(transaction, 'FDSFilters') == True:
        fdsfilters_data = []
        for filter in transaction.FDSFilters.FDSFilter:
            fdsfilter_data = {
                'name': f"{filter.name}",
                'value': f"{filter.value}",
            }
            fdsfilter_serializer = TransactionFDSFilterSerializer(data=fdsfilter_data)
            if fdsfilter_serializer.is_valid():
                fdsfilters_data.append(fdsfilter_serializer.validated_data)
            else:
                error_message = {"errors": fdsfilter_serializer.errors}
                raise ValueError(error_message)
        return fdsfilters_data
    return None
        
def get_order_data(transaction):
    if hasattr(transaction, 'order') == True:
        order = transaction.order
        order_data = {
            'invoiceNumber': f"{order.invoiceNumber}",
            'description': f"{order.description}",
            'purchaseOrderNumber': f"{order.purchaseOrderNumber}",
        }
        order_serializer = TransactionOrderSerializer(data=order_data)
        if order_serializer.is_valid():
            return order_serializer.validated_data
        error_message = {"errors": order_serializer.errors}
        raise ValueError(error_message)
    return None

def get_tax_data(transaction):
    if hasattr(transaction, 'tax') == True:
        tax = transaction.tax
        tax_data = {
            'amount': f"{tax.amount}",
            'name': f"{tax.name}",
            'description': f"{tax.description}",
        }
        tax_serializer = TransactionTaxSerializer(data=tax_data)
        if tax_serializer.is_valid():
            return tax_serializer.validated_data
        error_message = {"errors": tax_serializer.errors}
        raise ValueError(error_message)
    return None

def get_line_items_data(transaction):
    if hasattr(transaction, 'lineItems'):
        lineItems = transaction.lineItems
        line_items_data = []
        for lineItem in lineItems.lineItem:
            line_item_data = {
                'itemId': f"{lineItem.itemId}",
                'name': f"{lineItem.name}",
                'description': f"{lineItem.description}",
                'quantity': f"{lineItem.quantity}",
                'unitPrice': f"{lineItem.unitPrice}",
                'taxable': f"{lineItem.taxable}",
            }
            line_item_serializer = TransactionLineItemSerializer(data=line_item_data)
            if line_item_serializer.is_valid():
                line_items_data.append(line_item_serializer.validated_data)
            else:
                error_message = {"errors": line_item_serializer.errors}
                raise ValueError(error_message)
        return line_items_data
    return None

def get_payment_data(transaction):
    if hasattr(transaction, 'payment') == True:
        creditCard = transaction.payment.creditCard
        credit_card_data = {
            'cardNumber': f"{creditCard.cardNumber}",
            'expirationDate': f"{creditCard.expirationDate}",
            'cardType': f"{creditCard.cardType}",
        }
        credit_card_serializer = TransactionCreditCardSerializer(data=credit_card_data)
        if credit_card_serializer.is_valid():
            payment_data = {
                'creditCard': credit_card_serializer.validated_data,
            }
            payment_serializer = TransactionPaymentSerializer(data=payment_data)
            if payment_serializer.is_valid():
                return payment_serializer.validated_data
            error_message = {"errors": payment_serializer.errors}
            raise ValueError(error_message)
        error_message = {"errors": credit_card_serializer.errors}
        raise ValueError(error_message)
    return None
        
def get_customer_data(transaction):
    if hasattr(transaction, 'customer') == True:
        customer = transaction.customer
        customer_data = {
            'type': f"{customer.type}",
            'id': f"{customer.id}",
            'email': f"{customer.email}",
        }
        customer_serializer = TransactionCustomerSerializer(data=customer_data)
        if customer_serializer.is_valid():
            return customer_serializer.validated_data
        error_message = {"errors": customer_serializer.errors}
        raise ValueError(error_message)
    return None
        
def get_customer_address_data(transaction):
    if hasattr(transaction, 'billTo') == True:
        billTo = transaction.billTo
        customer_address_data = {
            'firstName': f"{billTo.firstName}",
            'lastName': f"{billTo.lastName}",
            'company': f"{billTo.company}",
            'address': f"{billTo.address}",
            'city': f"{billTo.city}",
            'state': f"{billTo.state}",
            'zip': f"{billTo.zip}",
            'country': f"{billTo.country}",
            'phoneNumber': f"{billTo.phoneNumber}",
            'faxNumber': f"{billTo.faxNumber}",
        }
        customer_address_serializer = TransactionCustomerAddressSerializer(data=customer_address_data)
        if customer_address_serializer.is_valid():
            return customer_address_serializer.validated_data
        error_message = {"errors": customer_address_serializer.errors}
        raise ValueError(error_message)
    return None

def build_transaction_data(transaction):
    transaction_data = {}
    fdsfilters_data = get_fdsfilters_data(transaction)
    if fdsfilters_data:
        transaction_data['FDSFilters'] = fdsfilters_data
    order_data = get_order_data(transaction)
    if order_data:
        transaction_data['order'] = order_data
    tax_data = get_tax_data(transaction)
    if tax_data:
        transaction_data['tax'] = tax_data
    line_items_data = get_line_items_data(transaction)
    if line_items_data:
        transaction_data['lineItems'] = line_items_data
    payment_data = get_payment_data(transaction)
    if payment_data:
        transaction_data['payment'] = payment_data
    customer_data = get_customer_data(transaction)
    if customer_data:
        transaction_data['customer'] = customer_data
    customer_addres_data = get_customer_address_data(transaction)
    if customer_addres_data:
        transaction_data['customerAddress'] = customer_addres_data
        
    # Add all other data
    transaction_data['transId'] = f"{transaction.transId}"
    transaction_data['submitTimeUTC'] = f"{transaction.submitTimeUTC}"
    transaction_data['submitTimeLocal'] = f"{transaction.submitTimeLocal}"
    transaction_data['transactionType'] = f"{transaction.transactionType}"
    transaction_data['transactionStatus'] = f"{transaction.transactionStatus}"
    transaction_data['responseCode'] = f"{transaction.responseCode}"
    transaction_data['responseReasonCode'] = f"{transaction.responseReasonCode}"
    transaction_data['responseReasonDescription'] = f"{transaction.responseReasonDescription}"
    transaction_data['authCode'] = f"{transaction.authCode}"
    transaction_data['AVSResponse'] = f"{transaction.AVSResponse}"
    transaction_data['cardCodeResponse'] = f"{transaction.cardCodeResponse}"
    transaction_data['authAmount'] = f"{transaction.authAmount}"
    transaction_data['settleAmount'] = f"{transaction.settleAmount}"
    transaction_data['taxExempt'] = f"{transaction.taxExempt}"

    return transaction_data
    
# !!!!!!!!GET TRANSACTION DETAILS END HERE!!!!!!!!! #


# !!!!!!!!CREATE PAYMENT DATA!!!!!!!!! #

def create_credit_card(data):
    creditCard = apicontractsv1.creditCardType()
    creditCardData = data.get('creditCard')
    credit_card_serializer = CreditCardSerializer(data=creditCardData)
    if credit_card_serializer.is_valid():
        creditCard.cardNumber = creditCardData.get('cardNumber') #"4111111111111111"
        creditCard.expirationDate = creditCardData.get('expirationDate') #"2035-12"
        creditCard.cardCode = creditCardData.get('cardCode') #"123"
        return creditCard
    error_message = {"errors": credit_card_serializer.errors}
    raise ValueError(error_message)

def create_order(data):
    order = apicontractsv1.orderType()
    orderData = data.get('order')
    order_serializer = None
    if orderData:
        order_serializer = OrderSerializer(data=orderData)
        if order_serializer.is_valid():
            order.invoiceNumber = orderData.get('invoice_number') #"10101"
            order.description = orderData.get('description') #"Golf Shirts"
            return order
        error_message = {"errors": order_serializer.errors}
        raise ValueError(error_message)
    return order

def create_customer_address(data):
    customerAddress = apicontractsv1.customerAddressType()
    customerAddressData = data.get('customerAddress')
    customer_address_serializer = None
    if customerAddressData:
        customer_address_serializer = CustomerAddressSerializer(data=customerAddressData)
        if customer_address_serializer.is_valid():
            customerAddress.firstName = customerAddressData.get('firstName') #"Ellen"
            customerAddress.lastName = customerAddressData.get('lastName') #"Johnson"
            customerAddress.company = customerAddressData.get('company') #"Souveniropolis"
            customerAddress.address = customerAddressData.get('address') #"14 Main Street"
            customerAddress.city = customerAddressData.get('city') #"Pecan Springs"
            customerAddress.state = customerAddressData.get('state') #"TX"
            customerAddress.zip = customerAddressData.get('zip') #"44628"
            customerAddress.country = customerAddressData.get('country') #"USA"
            return customerAddress
        error_message = {"errors": customer_address_serializer.errors}
        raise ValueError(error_message)
    return customerAddress

def create_customer_data(data):
    customerData = apicontractsv1.customerDataType()
    customerDataData = data.get('customerData')
    customer_data_serializer = None
    if customerDataData:
        customer_data_serializer = CustomerDataSerializer(data=customerDataData)
        if customer_data_serializer.is_valid():
            customerData.type = customerDataData.get('type') #"individual"
            customerData.id = customerDataData.get('id') #"99999456654"
            customerData.email = customerDataData.get('email') #"EllenJohnson@example.com"
            return customerData
        error_message = {"errors": customer_data_serializer.errors}
        raise ValueError(error_message)
    return customerData

def create_settings(data):
    settings = apicontractsv1.ArrayOfSetting()
    settingsData = data.get('settings')
    settings_serializer = []
    if settingsData:
        for settingData in settingsData:
            setting_serializer = SettingSerializer(data=settingData)
            if setting_serializer.is_valid():
                settings_serializer.append(setting_serializer)
                setting = apicontractsv1.settingType()
                setting.settingName = settingData.get('settingName')
                setting.settingValue = settingData.get('settingValue')
                settings.setting.append(setting)
            else:
                error_message = {"errors": setting_serializer.errors}
                raise ValueError(error_message)
        return settings
    return settings

def create_line_items(data):
    lineItems = apicontractsv1.ArrayOfLineItem()
    # setup individual line items
    lineItemsData = data.get('lineItems')
    line_items_serializer = []
    if lineItemsData:
        for lineItemData in lineItemsData:
            item_serializer = ItemSerializer(data=lineItemData)
            if item_serializer.is_valid():
                line_items_serializer.append(item_serializer)
                lineItem = apicontractsv1.lineItemType()
                lineItem.itemId = lineItemData.get('itemId')
                lineItem.name = lineItemData.get('name')
                lineItem.description = lineItemData.get('description')
                lineItem.quantity = lineItemData.get('quantity')
                lineItem.unitPrice = lineItemData.get('unitPrice')
                lineItem.taxable = lineItemData.get('taxable')
                lineItems.lineItem.append(lineItem)
            else:
                error_message = {"errors": line_items_serializer.errors}
                raise ValueError(error_message)
        return lineItems
    return lineItems

# !!!!!!!!CREATE PAYMENT END HERE!!!!!!!!! #