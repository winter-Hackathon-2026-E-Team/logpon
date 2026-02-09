# プログラム複製、バリデーション
from django import forms
from ...models.program_run import ProgramRun

class CreateForm(forms.ModelForm):
    class Meta:
        model = ProgramRun
        fields = ['user', 'program']
    
    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id')
        program_id = cleaned_data.get('program_id')
        if not user_id or not program_id:
            raise forms.ValidationError('ログイン状態でないか、プログラムが選択されていません。')
