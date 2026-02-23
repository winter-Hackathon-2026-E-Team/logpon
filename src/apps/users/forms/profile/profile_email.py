from django import forms
from django.forms import ModelForm
from ...models.users import User

class ProfileEmailForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        print('emailバリデーション')
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('このメールアドレスは既に登録されています')
        return email.lower().strip()
