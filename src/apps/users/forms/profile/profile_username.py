from django.forms import ModelForm
from ...models.users import User
from django import forms

class ProfileUsernameForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']

