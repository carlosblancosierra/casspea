from django import forms
from .models import ShippingType

class ShippingTypeForm(forms.ModelForm):
    class Meta:
        model = ShippingType
        fields = ['name']
