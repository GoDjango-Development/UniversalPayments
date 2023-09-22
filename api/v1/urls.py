from django.urls import path
from api.v1.views.bank_of_america_payments import AllBoAPayments, BoAPaymentByTransactionUUID, CreateBoAPayment
from api.v1.views.square_payments import AllSquarePayments, CreateSquarePayment, SquarePaymentByTransactionUUID
from api.v1.views.wells_fargo_payment import AllWFPayments, CreateWFPayment, WFPaymentByTransactionUUID 
from api.v1.views.security import LoginView

urlpatterns = [
    path('auth/', LoginView.as_view()),
    path('create_wf_payments/', CreateWFPayment.as_view()),
    path('all_wf_payments/', AllWFPayments.as_view()),
    path('wf_payments/<str:transaction_uuid>', WFPaymentByTransactionUUID.as_view()),
    path('create_square_payments/',CreateSquarePayment.as_view()),
    path('all_square_payments/',AllSquarePayments.as_view()),
    path('square_payments/<str:idempotency_key>', SquarePaymentByTransactionUUID.as_view()),
    path('create_boa_payments/', CreateBoAPayment.as_view()),
    path('all_boa_payments/', AllBoAPayments.as_view()),
    path('boa_payments/<str:transaction_uuid>', BoAPaymentByTransactionUUID.as_view()),
]
