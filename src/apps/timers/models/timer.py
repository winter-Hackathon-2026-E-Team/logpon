from django.db import models
from apps.timers.models.sound import Sound


class Timer(models.Model):
    class Category(models.TextChoices):
        FOCUS = "focus", "集中"
        BREAK = "break", "休憩"
        REFRESH = "refresh", "リフレッシュ"

    name = models.CharField(max_length=50)

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
    )

    # 内部は秒で保持（UIは分でもOKだが保存は秒が楽）
    duration_seconds = models.PositiveIntegerField()

    # Soundは開発側で用意。削除されたらタイマー側はNULLにするのが安全
    sound = models.ForeignKey(
        Sound,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="timers",
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "timers"

    def __str__(self) -> str:
        return self.name
