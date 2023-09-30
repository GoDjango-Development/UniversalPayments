from django import forms
from documentation.models import StripeDocumentation
from ckeditor.widgets import CKEditorWidget


class StripeDocumentationForm(forms.ModelForm):
    class Meta:
        model = StripeDocumentation
        
        fields = '__all__'

        widgets = {
            'documentation': CKEditorWidget(attrs={'disable': True})
        }