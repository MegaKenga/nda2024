from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'}))
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'example@example.ru'}))
    details = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False, 'allow_empty_file': True}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Ваше сообщение'}))
