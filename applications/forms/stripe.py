from django import forms
from applications.models import StripeApplication


class StripeApplicationForm(forms.ModelForm):
    custom_header = forms.CharField(label='DATOS DE STRIPE', disabled=True, required=False, widget=forms.TextInput(attrs={'style': 'display:none;'}))
    
    class Meta:
        model = StripeApplication

        fields = ['client_id', 'client_secret', 'name', 'custom_header', 'api_public_key','api_secret_key']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'data-show-length': True}),
            'client_id': forms.TextInput(attrs={'class': 'form-control', 'data-show-length': True}),
            'client_secret': forms.TextInput(attrs={'class': 'form-control', 'data-show-length': True})
        }

        labels = {
            'name': 'nombre',
            'client_secret': 'secreto de cliente',
            'client_id': 'ID de cliente'
        }