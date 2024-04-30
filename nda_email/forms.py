import re

from django import forms
from django.core.exceptions import ValidationError


class ContactForm(forms.Form):
    name = forms.CharField(required=True, max_length=120, widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}))
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'example@example.ru'}))
    company_details = forms.FileField(required=False, widget=forms.ClearableFileInput(
        attrs={'multiple': False, 'allow_empty_file': True}))
    message = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'Ваше сообщение'}))

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        correct_phone_number = r'(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?'
        if not re.match(correct_phone_number, phone_number):
            raise ValidationError('Проверьте правильно ли введен номер')
        return phone_number

    def clean_email(self):
        email = self.cleaned_data['email']
        correct_email = r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)'
        if not re.match(correct_email, email):
            raise ValidationError('Проверьте правильно ли указана почта для обратной связи')
        return email

