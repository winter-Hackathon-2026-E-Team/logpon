from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django import forms
from apps.timers.models import Timer


class TimerForm(forms.ModelForm):
    # 画面入力は「分」(DBは秒)
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
        fields = ["name", "category", "sound", "is_active"]
        # sound は blank=True なので未選択OKの<select>になる

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 編集時：秒→分を初期値に
        if self.instance and self.instance.pk:
            minutes = Decimal(self.instance.duration_seconds) / Decimal("60")
            self.fields["duration_minutes"].initial = minutes.quantize(
                Decimal("0.1"), rounding=ROUND_HALF_UP
            )

    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()
        if not name:
            raise forms.ValidationError("名前が空です")
        if len(name) > 50:
            raise forms.ValidationError("名前は50文字以内です")
        return name

    def clean_duration_minutes(self):
        raw = self.cleaned_data["duration_minutes"]
        max_sec = 24 * 60 * 60  # 24時間

        try:
            seconds = int((raw * Decimal("60")).to_integral_value(rounding=ROUND_HALF_UP))
        except (InvalidOperation, ValueError):
            raise forms.ValidationError("分の値が不正です")

        if seconds <= 0:
            raise forms.ValidationError("分は0より大きい値にしてください")

        if seconds > max_sec:
            raise forms.ValidationError("分は24時間以内にしてください")

        self._duration_seconds = seconds
        return raw

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.duration_seconds = getattr(self, "_duration_seconds", obj.duration_seconds)
        if commit:
            obj.save()
        return obj

