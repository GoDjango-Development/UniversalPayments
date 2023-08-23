from django import forms
from payments.models import SquaresPayment


class SquarePaymentForm(forms.ModelForm):
    
    class Meta:
        model = SquaresPayment

        exclude = ('user',)