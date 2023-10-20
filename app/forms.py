from django import forms
from django.core.validators import RegexValidator
class ShippingAddressForm(forms.Form):
    address = forms.CharField(max_length=200, required=True)
    city = forms.CharField(max_length=200, required=True)
    recipient_name = forms.CharField(max_length=200, required=True)
    
    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Vui lòng nhập đúng",
    )
    mobile = forms.CharField(
        validators=[phone_regex],
        max_length=10,
        required=True,
        error_messages={
            'invalid': 'Vui lòng nhập số hợp lệ.',
        }
    )