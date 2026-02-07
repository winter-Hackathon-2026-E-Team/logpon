from django.db import models
from .program_run import ProgramRun

class TimerRun(models.Model):
    class Meta:
        db_table = 'timer_runs'
    
    class Status(models.TextChoices):
        PENDING = 'pending', '初期状態'
        RUNNING = 'running', '実行中'
        PAUSED = 'paused', '一時停止中'
        FINISHED = 'finished', '完了'
        SKIPPED = 'skipped', 'スキップ'
        INTERRUPTED = 'interrupted', '中断'
    
    order_index_snapshot = models.IntegerField()
    timer_name_snapshot = models.CharField(max_length=255)
    duration_sec_snapshot = models.IntegerField()
    sound_file_snapshot = models.CharField(max_length=255)
    category_snapshot = models.CharField(max_length=255)
    timer_status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    started_at = models.DateTimeField(null=True)
    ended_a = models.DateTimeField(null=True)
    paused_at = models.DateTimeField(null=True)
    elapsed_sec = models.IntegerField(null=True)
    memo = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    program_run = models.ForeignKey(
        to=ProgramRun,
        on_delete=models.CASCADE,
        related_name='timer_runs',
    )
