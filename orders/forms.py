import re

from django import forms


class CreateOrderForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Ivan'}
    ))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Ivanov'}
    ))
    phone = forms.RegexField(
        regex=r"^((\+7|7|8)+([0-9]){10})$",
        error_messages={'invalid': 'Phone number is incorrect'},
        widget=forms.TextInput(attrs={'placeholder': '8 XXX XXX-XX-XX'})
    )
    city = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Moscow'}
    ))
    street = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Pushkina'}
    ))
    house = forms.CharField(max_length=5, widget=forms.TextInput(
        attrs={'placeholder': '25'}
    ))
    apartment = forms.CharField(max_length=5, widget=forms.TextInput(
        attrs={'placeholder': '81'}
    ))
    postal_code = forms.CharField(
        max_length=6, min_length=6,
        widget=forms.TextInput(attrs={'placeholder': '198510'})
    )
