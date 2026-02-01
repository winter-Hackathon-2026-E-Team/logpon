from django.urls import path

from .views import program_runs, records, daily_reports

app_name = 'runs'
urlpatterns = [
    path('program-runs/', program_runs.ProgramRunsView.as_view(), name='program-runs'),
    path('records/', records.RecordsView.as_view(), name='records'),
    path('daily-reports/', daily_reports.DailyReportsView.as_view(), name='daily-reports')
]
