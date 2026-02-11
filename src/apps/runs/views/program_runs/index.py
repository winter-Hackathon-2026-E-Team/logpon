# /program-runs/のGET（表示）, program_idのPOST（draft作成）
import json
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse
from ...models.program_run import ProgramRun
from ....programs.models.program import Program
from ...selectors.program_runs import selector_exist_runs
from ...serializers.program_runs import serialize_exist_runs
from ...services.program_runs.create_draft import create_runs_draft

class ProgramRunsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'runs/test_program-runs.html')

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        program_id = body.get('program_id')

        if not ProgramRun.objects.filter(program_id=program_id).exists():
            program = Program.objects.filter(id=program_id, user=request.user).first()
            if program is None:
                return JsonResponse({'error': 'invalid program'}, status=400)
            create_runs_draft(user=request.user, program=program)

        program_run, timer_runs, program_run_id = selector_exist_runs(program_id)
        data = serialize_exist_runs(program_run, timer_runs)
        url = reverse('runs:program-runs-detail', kwargs={'program_run_id': program_run_id})
        return JsonResponse({'redirect_url': url, 'data': data})
