from django import forms
from django.forms import NumberInput
from django.core.mail import send_mail
from nda.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, RECIPIENT_EMAIL


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, widget=NumberInput(attrs={'placeholder': '1', }))


class GetOrderForm(forms.Form):

    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
