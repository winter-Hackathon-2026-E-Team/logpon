# /program-runs/のGET（表示）, program_idのPOST（draft作成）
import json
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from ...models.program_run import ProgramRun
from ....programs.models.program_timer import ProgramTimer
from ...forms.program_runs.create import CreateForm

class ProgramRunsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'runs/test_program-runs.html')

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        program_id = body.get('program_id')
        print(type(body), body)
        print(program_id)
        print(ProgramRun.objects.values())
        print(ProgramRun.objects.filter(program_id=program_id).values())

        if ProgramRun.objects.filter(program_id=program_id).values():
            data = ProgramRun.objects.filter(program_id=program_id)
        else:
            data = ProgramTimer.objects.filter(program_id=program_id)
            form = CreateForm(data)

        return redirect('runs:program-runs-detail')
