from crm.models import Client
from django import forms


class CreateClientForm(forms.Form):
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    sex = forms.ChoiceField(choices=Client.SEX_CHOICES, required=True)
    birth_date = forms.DateField(required=False, input_formats=['%d.%m.%Y',])
    phone = forms.CharField(max_length=255)
    mail = forms.EmailField(required=False)

    def model(self):
        if not self.is_valid():
            return None

        c = Client()
        c.first_name = self.cleaned_data['first_name']
        c.last_name = self.cleaned_data['last_name']
        c.sex = self.cleaned_data['sex']
        c.birth_date = self.cleaned_data['birth_date']
        c.phone = self.cleaned_data['phone']
        c.mail = self.cleaned_data['mail']
        return c
