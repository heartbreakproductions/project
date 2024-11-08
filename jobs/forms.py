# jobs/forms.py
from django import forms
from .models import Country, State, City

class JobSearchForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required=False)
    state = forms.ModelChoiceField(queryset=State.objects.all(), required=False)
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=False)
    description = forms.CharField(max_length=100, required=False)
