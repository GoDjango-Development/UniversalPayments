from django import forms
from applications.models import SquaresApplication


class SquareApplicationForm(forms.ModelForm):
    custom_header = forms.CharField(label='DATOS DE SQUARE', disabled=True, required=False, widget=forms.TextInput(attrs={'style': 'display:none;'}))
    
    class Meta:
        model = SquaresApplication

        fields = ['client_id', 'client_secret', 'name', 'custom_header', 'access_token', 'environment', 'application_id', 'location_id']

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