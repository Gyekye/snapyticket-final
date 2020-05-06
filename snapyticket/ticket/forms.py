from django.forms import ModelForm
from .models import TicketItem


class AddToCartForm(ModelForm):
    class Meta:
        model = TicketItem
        fields = [
            'quantity'
        ]