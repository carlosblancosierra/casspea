from django import forms

from .models import CustomBoxLogo


class CustomBoxLogoForm(forms.ModelForm):
    class Meta:
        model = CustomBoxLogo
        fields = ['image']
