from django import forms
from datetime import timedelta, date
from .models import Menu


class MenuForm(forms.ModelForm):
    today = date.today()
    created_date = forms.DateField(initial=today, disabled=True)
    expiration_date = forms.DateField(widget=forms.SelectDateWidget,
                                      required=True,
                                      initial=timedelta(days=1))
    season = forms.CharField(max_length=20, required=True)

    class Meta:
        model = Menu
        fields = ['season', 'items', 'expiration_date', 'created_date']

    def clean(self):
        cleaned_data = super().clean()
        cleaned_expiration_date = cleaned_data.get('expiration_date')
        cleaned_created_date = cleaned_data.get('created_date')
        cleaned_items = cleaned_data.get('items')

        # check expiration date is after created date
        if cleaned_expiration_date:
            if cleaned_created_date >= cleaned_expiration_date + timedelta(days=1):
                raise forms.ValidationError(
                    "Expiration Date cannot be before created date"
                )

        if not cleaned_items:
            raise forms.ValidationError("An item must be selected")

        return cleaned_data




