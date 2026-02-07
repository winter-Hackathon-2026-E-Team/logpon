from django.urls import path

from .views.program_runs import (
    ProgramRunsView,
    ProgramDraftView,
    ProgramStartView,
    ProgramResumeView,
    ProgramPauseView,
    ProgramSkipView,
    ProgramNextView,
    ProgramInterruptView,
    ProgramProgressView,
)

from .views import timer_runs, records, daily_reports

app_name = 'runs'
urlpatterns = [
    # プログラム実行
    path('program-runs/', ProgramRunsView.as_view(), name='program-runs'),
    path('program-runs/draft/', ProgramDraftView.as_view(), name='program-runs-draft'),
    path('program-runs/<int:program_run_id>/start/', ProgramStartView.as_view(), name='program-runs-start'),
    path('program-runs/<int:program_run_id>/resume/', ProgramResumeView.as_view(), name='program-runs-resume'),
    path('program-runs/<int:program_run_id>/pause/', ProgramPauseView.as_view(), name='program-runs-pause'),
    path('program-runs/<int:program_run_id>/skip/', ProgramSkipView.as_view(), name ='program-runs-skip'),
    path('program-runs/<int:program_run_id>/next/', ProgramNextView.as_view(), name ='program-runs-next'),
    path('program-runs/<int:program_run_id>/interrupt/', ProgramInterruptView.as_view(), name ='program-runs-interrupt'),
    path('program-runs/<int:program_run_id>/progress/', ProgramProgressView.as_view(), name ='program-runs-progress'),

    # タイマーメモ
    path('timer-runs/<int:timer_run_id>/memo/', timer_runs.memo.TimerRunsMemoView.as_view(), name='timer-runs-memo'),

    # 実施記録確認
    path('records/', records.RecordsView.as_view(), name='records'),

    # 日報
    path('daily-reports/', daily_reports.DailyReportsView.as_view(), name='daily-reports'),
]
