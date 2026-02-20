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

# プログラムpause（一時停止）
@transaction.atomic
def status_pause(program_run_id, timer_run_id, elapsed_sec:int):
    program_run = ProgramRun.objects.select_for_update().get(id=program_run_id)
    program_run.status = ProgramRun.Status.PAUSED
    program_run.paused_at = timezone.now()
    program_run.updated_at = timezone.now()
    program_run.save()

    timer_run = TimerRun.objects.select_for_update().get(id=timer_run_id, program_run_id=program_run_id)
    timer_run.status = TimerRun.Status.PAUSED
    timer_run.paused_at = timezone.now()
    timer_run.elapsed_sec += elapsed_sec
    timer_run.updated_at = timezone.now()
    timer_run.save()

# プログラムresume（再開）
@transaction.atomic
def status_resume(program_run_id, timer_run_id, elapsed_sec:int):
    program_run = ProgramRun.objects.select_for_update().get(id=program_run_id)
    program_run.status = ProgramRun.Status.RUNNING
    program_run.updated_at = timezone.now()
    program_run.save()

    timer_run = TimerRun.objects.select_for_update().get(id=timer_run_id, program_run_id=program_run_id)
    timer_run.status = TimerRun.Status.RUNNING
    timer_run.elapsed_sec += elapsed_sec
    timer_run.updated_at = timezone.now()
    timer_run.save()

# プログラムnext（自動遷移）
@transaction.atomic
def status_next(program_run_id, timer_run_id, elapsed_sec:int):
    timer_run = TimerRun.objects.select_for_update().get(id=timer_run_id, program_run_id=program_run_id)
    timer_run.status = TimerRun.Status.FINISHED
    timer_run.ended_at = timezone.now()
    timer_run.elapsed_sec += elapsed_sec
    timer_run.updated_at = timezone.now()
    timer_run.save()

    next_order_index = timer_run.order_index_snapshot + 1
    is_next_timer = TimerRun.objects.filter(program_run_id=program_run_id, order_index_snapshot=next_order_index).exists()

    if is_next_timer:
        next_timer = TimerRun.objects.select_for_update().get(program_run_id=program_run_id, order_index_snapshot=next_order_index)
        next_timer.status = TimerRun.Status.RUNNING
        next_timer.started_at = timezone.now()
        next_timer.updated_at = timezone.now()
        next_timer.save()
        return next_timer

    else:
        program_run = ProgramRun.objects.select_for_update().get(id=program_run_id)
        program_run.status = ProgramRun.Status.FINISHED
        program_run.ended_at = timezone.now()
        program_run.updated_at = timezone.now()
        program_run.save()

    return None