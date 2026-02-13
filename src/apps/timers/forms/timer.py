from decimal import Decimal, ROUND_HALF_UP
from django import forms

from apps.timers.models import Timer


class TimerForm(forms.ModelForm):
    duration_minutes = forms.DecimalField(
        label="分",
        min_value=Decimal("0.1"),
        max_value=Decimal("1440"),
        decimal_places=1,
        max_digits=6,
        required=True,
    )

    class Meta:
        model = Timer
        # duration_seconds はフォームに出さず、duration_minutes から計算して保存する
        fields = ["name", "category", "duration_minutes", "sound"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 編集画面用：DBの秒→分にして初期表示
        if self.instance and self.instance.pk and self.instance.duration_seconds is not None:
            self.fields["duration_minutes"].initial = (
                Decimal(self.instance.duration_seconds) / Decimal("60")
            ).quantize(Decimal("0.1"))

    def save(self, *, user=None, commit=True):
        obj: Timer = super().save(commit=False)

        minutes = self.cleaned_data["duration_minutes"]
        seconds = (minutes * Decimal("60")).to_integral_value(rounding=ROUND_HALF_UP)
        obj.duration_seconds = int(seconds)

        # 作成時は user 必須、更新時は既存の obj.user を維持
        if obj.pk is None:
            if user is None:
                raise TypeError("TimerForm.save() missing required keyword-only argument: 'user'")
            obj.user = user

        if commit:
            obj.save()
            self.save_m2m()
        return obj

