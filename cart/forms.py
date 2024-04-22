from django import forms
from django.core.exceptions import ValidationError
from django.forms import NumberInput


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, widget=NumberInput(attrs={'placeholder': '1', }))


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120, label="Ваше имя")
    phone_number = forms.CharField(max_length=120)
    email = forms.EmailField()
    subject = forms.CharField(max_length=70)
    message = forms.CharField(widget=forms.Textarea)

    def clean_name(self):
        data = self.cleaned_data["name"]
        if len(data) < 3:
            raise ValidationError("Должно быть больше 3 символов")
        return data
