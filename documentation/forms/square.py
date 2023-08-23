from django import forms
from documentation.models import SquaresDocumentation
from ckeditor.widgets import CKEditorWidget


class SquareDocumentationForm(forms.ModelForm):
    class Meta:
        
        model = SquaresDocumentation
        
        fields = '__all__'

        widgets = {
            'documentation': CKEditorWidget(attrs={'disable': True})
        }