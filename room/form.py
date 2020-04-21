from django import forms
from room import models


class RegisterForm(forms.Form):
    def choice():
        c=[(choice.pk, choice.title) for choice in models.EdLevel.objects.all()]
        return c

    email=forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Email'}))
    firstname=forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': "form-control", 'placeholder': 'Enter Full Name'}))
    lastname=forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': "form-control", 'placeholder': 'Enter Full Name'}))
    password=forms.CharField(widget=forms.PasswordInput(
        attrs={'class': "form-control", 'placeholder': 'Enter Password'}))
    edlevel=forms.ChoiceField(required=True, choices=choice(), widget=forms.Select(attrs={'class': 'custom-select mr-sm-2'}))