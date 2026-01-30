from django.shortcuts import render, redirect
from django.views import View

class DailyReportsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'runs/daily-reports.html')

daily_reports = DailyReportsView.as_view()
