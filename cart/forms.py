from django import forms
from django.forms import NumberInput


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, widget=NumberInput(attrs={'placeholder': '1', }))


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    subject = forms.CharField(max_length=70)
    message = forms.CharField(widget=forms.Textarea)
