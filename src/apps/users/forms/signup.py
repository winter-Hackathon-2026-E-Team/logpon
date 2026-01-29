from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..models.users import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username',)
    
    def clean(self):
        super().clean()
        email = self.cleaned_data.get['email']
        username = self.cleaned_data.get['username']
        password1 = self.cleaned_data.get['password']
        password2 = self.cleaned_data.get['password2']

        if password1 != password2:
            raise forms.ValidationError('パスワードと確認用パスワードが一致しません')
        

