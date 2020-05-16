from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from voter.models import Voter

class CreateVoterForm(UserCreationForm):

    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'}))
    class Meta:
        model = User
        fields = ["username","email",'password1','password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Email'}),

        }
