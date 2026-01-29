from django import forms
from django.contrib.auth.forms import AuthenticationForm
from ..models.users import User

class LoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス', max_length=254, widget=forms.EmailInput(),)
    password = forms.CharField(label='パスワード', max_length=255, widget=forms.PasswordInput(),)

