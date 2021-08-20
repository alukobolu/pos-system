from django import forms
from django.forms import TextInput, Select, FileInput, NumberInput, Textarea

from base.models import ATM


class ProductForm(forms.ModelForm):
    class Meta:
        model = ATM
        fields = '__all__'
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'id': 'title', 'placeholder': 'Transaction type'}),
            'price': NumberInput(attrs={'class': 'form-control', 'id': 'price'}),
            'addon': NumberInput(attrs={'class': 'form-control', 'id': 'addon'}),
            'total_price': NumberInput(attrs={'class': 'form-control', 'id': 'total_price'}),
            'other_info': Textarea(attrs={'class': 'form-control', 'id': 'other_info'}),
        }
