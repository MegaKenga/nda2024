from django import forms


PHONE_PATTERN = r"^((\+?)(?:\d[^A-Z,a-z,@]{10,14}))$"
EMAIL_PATTERN = r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]{2,})"


class ContactForm(forms.Form):
    name = forms.CharField(
        required=False,
        max_length=120,
        widget=forms.TextInput(
            attrs={
                "placeholder": "ФИО контактного лица1",
                "class": "form-control",
                "id": "fullNameLegal",
            }
        ),
    )
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                # "placeholder": "Номер телефона",
                "class": "form-control phone-mask",
                "id": "validationPhoneNumber1",
         
            }
        ),
    )
    email = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "example@example.ru",
                "class": "form-control",
                "id": "email",
            }
        ),
    )

    company_name = forms.CharField(
        label="Наименование организации",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "companyName",
                "placeholder": "Наименование организации",
            }
        ),
    )

    inn = forms.CharField(
        label="ИНН",
        max_length=12,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "inn",
                "placeholder": "ИНН",
            }
        ),
    )

    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"id": "message", "class": "form-control","placeholder": "Комментарий к заказу"}),
    )

    company_details = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "multiple": False,
                "allow_empty_file": True,
                "id": "contact_form_company_details_input",
                "form": "cart_modal_form",
                "class": "form-control",
                "type": "file",
            }
        ),
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        return phone_number  # Просто возвращаем номер телефона без проверки

    def clean_email(self):
        email = self.cleaned_data["email"]
        return email  # Просто возвращаем email без проверки


class PhysicalContactForm(forms.Form):
    name = forms.CharField(
        required=False,
        max_length=120,
        widget=forms.TextInput(
            attrs={
                "placeholder": "ФИО контактного лица2",
                "class": "form-control",
                "id": "fullNameLegal",
            }
        ),
    )
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                # "placeholder": "Номер телефона",
                "class": "form-control phone-mask",
                "id": "validationPhoneNumber",
              
            }
        ),
    )
    email = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "example@example.ru",
                "class": "form-control",
                "id": "email",
            }
        ),
    )

    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"id": "message", "class": "form-control","placeholder": "Комментарий к заказу"}),
    )

    company_details = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "multiple": False,
                "allow_empty_file": True,
                "id": "p_contact_form_company_details_input",
                "form": "cart_modal_form",
                "class": "form-control",
                "type": "file",
            }
        ),
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        return phone_number  # Просто возвращаем номер телефона без проверки

    def clean_email(self):
        email = self.cleaned_data["email"]
        return email  # Просто возвращаем email без проверки


class MailForm(forms.Form):
    name = forms.CharField(
        required=True,
        max_length=120,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ваше имя *",
                "class": "form-control",
                "id": "fullNameLegal",
            }
        ),
    )
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Номер телефона",
                "class": "form-control phone-mask",
                "id": "validationPhoneNumber",
         
            }
        ),
    )
    email = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ваш email *",
                "class": "form-control",
                "id": "email",
            }
        ),
    )

    company_name = forms.CharField(
        label="Название организации",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "companyName",
                "placeholder": "Наименование организации",
            }
        ),
    )

    inn = forms.CharField(
        label="ИНН",
        max_length=12,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "inn",
                "placeholder": "ИНН",
            }
        ),
    )

    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"id": "message", "class": "form-control", "placeholder": "Текст письма *"}),
    )

    company_details = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "multiple": False,
                "allow_empty_file": True,
                "id": "mail_form_company_details_input",
                "form": "cart_modal_form",
                "class": "form-control",
                "type": "file",
            }
        ),
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        return phone_number  # Просто возвращаем номер телефона без проверки

    def clean_email(self):
        email = self.cleaned_data["email"]
        return email  # Просто возвращаем email без проверки

    

class CallForm(forms.Form):
    name = forms.CharField(
        required=True,
        max_length=120,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ваше имя",
                "class": "form-control",
            }
        ),
    )
    phone_number = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Номер телефона",
                "class": "form-control",
            }
        ),
    )
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"id": "message", "class": "form-control", "placeholder": "Комментарии",}),
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        return phone_number  # Просто возвращаем номер телефона без проверки

    def clean_email(self):
        email = self.cleaned_data["email"]
        return email  # Просто возвращаем email без проверки
