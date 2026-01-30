from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..models.users import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username',) # パスワードはハッシュ化するため指定しない
