from django import forms
from runsala.models import Repository


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class NewRepositoryForm(forms.ModelForm):
    class Meta:
        model = Repository
