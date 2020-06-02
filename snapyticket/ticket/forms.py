from django.forms import ModelForm
from .models import TicketItem
from django import forms


class AddToCartForm(ModelForm):
    quantity = forms.IntegerField(label='', widget=forms.NumberInput(attrs={
        'value': '1'
    }))
    class Meta:
        model = TicketItem
        fields = [
            'quantity'
        ]