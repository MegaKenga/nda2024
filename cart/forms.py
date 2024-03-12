from django import forms
from django.forms import NumberInput
from django.core.mail import send_mail
from nda.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, RECIPIENT_EMAIL


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, widget=NumberInput(attrs={'placeholder': '1', }))


class ContactForm(forms.Form):

    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    inquiry = forms.CharField(max_length=70)
    message = forms.CharField(widget=forms.Textarea)

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()

        name = cl_data.get('name').strip()
        from_email = cl_data.get('email')
        subject = cl_data.get('inquiry')

        msg = f'{name} with email {from_email} said:'
        msg += f'\n"{subject}"\n\n'
        msg += cl_data.get('message')

        return subject, msg

    def send(self):
        subject, msg = self.get_info()
        send_mail(
            subject=subject,
            message=msg,
            from_email=EMAIL_HOST_USER,
            auth_password=EMAIL_HOST_PASSWORD,
            recipient_list=[RECIPIENT_EMAIL]
        )
