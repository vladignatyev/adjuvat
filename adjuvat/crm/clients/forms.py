from crm.models import Client
from django import forms


class CreateClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['company']

    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    sex = forms.ChoiceField(choices=Client.SEX_CHOICES, required=True)
    birth_date = forms.DateField(required=False, input_formats=['%d.%m.%Y'],
                                 widget=forms.widgets.DateInput(format='%d.%m.%Y'))
    phone = forms.CharField(max_length=255)
    mail = forms.EmailField(required=False)
