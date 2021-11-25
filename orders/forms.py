import re

from django import forms


class CreateOrderForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone = forms.RegexField(
        regex=r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$",
        error_messages={'invalid': 'Phone number is incorrect'}
    )
    city = forms.CharField(max_length=100)
    street = forms.CharField(max_length=100)
    house = forms.CharField(max_length=5)
    apartment = forms.CharField(max_length=5)
    postal_code = forms.CharField(max_length=6, min_length=6)
