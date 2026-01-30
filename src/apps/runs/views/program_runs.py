from django.shortcuts import render, redirect
from django.views import View

class ProgramRunsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'runs/program-runs.html')

program_runs = ProgramRunsView.as_view()
