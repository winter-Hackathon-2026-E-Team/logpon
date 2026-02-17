# DB検索、取得（読み取り専用）
from ...programs.models import Program, ProgramTimer
from ..models.program_run import ProgramRun
from ..models.timer_run import TimerRun

# 既存のすべてのprograms取得
def selector_exist_programs(user_id):
    programs = Program.objects.filter(user_id=user_id).values().all()
    return programs

# 既存のprogram_runs, timer_runs取得
def selector_exist_runs(program_run_id):
    program_run = ProgramRun.objects.filter(id=program_run_id).values(
        'id',
        'program_id',
        'status',
        ).first()
    timer_runs = TimerRun.objects.filter(program_run_id=program_run_id).values(
        'id',
        'order_index_snapshot',
        'timer_name_snapshot',
        'duration_sec_snapshot',
        'category_snapshot',
        'status',
        'elapsed_sec',
        )
    return (program_run, timer_runs)
