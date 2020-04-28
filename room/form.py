from django import forms
from room import models


class RegisterForm(forms.Form):

    email=forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Email'}))
    firstname=forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': "form-control", 'placeholder': 'Enter Full Name'}))
    lastname=forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': "form-control", 'placeholder': 'Enter Full Name'}))
    password=forms.CharField(widget=forms.PasswordInput(
        attrs={'class': "form-control", 'placeholder': 'Enter Password'}))