# start/resume/pause/skip/step_next/interruptの状態変更サービス層
from django.db import transaction
from django.utils import timezone
from apps.runs.models import ProgramRun, TimerRun

# プログラムstart（初回実行）
@transaction.atomic
def status_start(program_run_id, timer_run_id):
    program_run = ProgramRun.objects.select_for_update().get(id=program_run_id)
    program_run.status = ProgramRun.Status.RUNNING
    program_run.started_at = timezone.now()
    program_run.updated_at = timezone.now()
    program_run.save()

    timer_run = TimerRun.objects.select_for_update().get(id=timer_run_id, program_run_id=program_run_id)
    timer_run.status = TimerRun.Status.RUNNING
    timer_run.started_at = timezone.now()
    timer_run.updated_at = timezone.now()
    timer_run.save()
