from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomerRegistationForm(UserCreationForm):
  username = forms.CharField(widget=forms.TextInput(attrs={"autofocus": 'True', 'class': 'form-control'}))
  email = forms.EmailField(widget=forms.EmailInput(attrs={"autofocus": 'True', 'class': 'form-control'}))
  password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"autofocus": 'True', 'class': 'form-control'}))
  password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={"autofocus": 'True', 'class': 'form-control'}))

  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']
