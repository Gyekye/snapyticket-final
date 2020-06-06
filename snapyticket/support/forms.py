from django import forms
from .models import Contact

MESSAGE_SUBJECT = (
    ('TP', "Technical Problems"),
    ('RP', "Refund Problems"),
    ('OP', "Other Problems"),
)

class ContactForm(forms.ModelForm):
     class Meta:
          model = Contact
          fields = [
               'fullname',
               'subject',
               'email',
               'message',
          ]