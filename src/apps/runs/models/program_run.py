from django.db import models
from django.conf import settings

class ProgramRun(models.Model):
    class Meta:
        db_table = 'program_runs'
    
    class Status(models.TextChoices):
        # value, labelのタプル形式
        DRAFT = 'draft', '下書き'
        START = 'start', '実行中'
        RESUME = 'resume', '実行中'
        PAUSE = 'pause', '一時停止中'
        FINISH = 'finish', '完了'
        INTERRUPT = 'interrupt', '中断'

    program_name_snapshot = models.CharField(max_length=255)
    program_status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    started_at = models.DateTimeField(null=True)
    ended_at = models.DateTimeField(null=True)
    paused_at = models.DateTimeField(null=True)
    total_elapsed_sec = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='program_runs',
    )
