from django import forms

from apps.investment.models import Investment


class FormInvestment(forms.ModelForm):
    class Meta:
        model = Investment
        fields = '__all__'
        widgets = {
            'amount_crypto': forms.NumberInput(attrs={'readonly': True})
        }
