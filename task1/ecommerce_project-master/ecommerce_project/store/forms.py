# store/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email      = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name  = forms.CharField(max_length=50)

    class Meta:
        model  = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')


class CheckoutForm(forms.Form):
    full_name   = forms.CharField(max_length=200)
    email       = forms.EmailField()
    address     = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    city        = forms.CharField(max_length=100)
    country     = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=20)