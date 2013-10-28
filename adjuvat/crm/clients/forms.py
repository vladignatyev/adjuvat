from crm.models import Client
from django import forms


class CreateClientForm(forms.Form):
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    sex = forms.ChoiceField(choices=Client.SEX_CHOICES, required=True)
    birth_date = forms.DateField()
    phone = forms.CharField(max_length=255)
    mail = forms.EmailField(required=False)

    def model(self):
        if not self.is_valid():
            return None

        c = Client()
        c.first_name = self.first_name
        c.last_name = self.last_name
        c.sex = self.sex
        c.birth_date = self.birth_date
        c.phone = self.phone
        c.mail = self.mail
        return c
