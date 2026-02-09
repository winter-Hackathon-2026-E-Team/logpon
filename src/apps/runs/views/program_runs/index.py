# /program-runs/のGET（表示）, program_idのPOST（draft作成）
import json
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from ...models.program_run import ProgramRun
from ....programs.models.program_timer import ProgramTimer
from ...forms.program_runs.create import CreateForm
from ...selectors.program_runs import selector_exist
from ...serializers.program_runs import serialize_initial

class ProgramRunsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'runs/test_program-runs.html')

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        program_id = body.get('program_id')

        if ProgramRun.objects.filter(program_id=program_id):
            program_run, timer_runs, program_run_id = selector_exist(program_id)
        else:
            program_timers = ProgramTimer.objects.filter(program_id=program_id).order_by('order_index').values()
            print(program_timers)
            # form = CreateForm(data)

        data = serialize_initial(program_run, timer_runs)
        print(data)
        url = reverse_lazy('runs:program-runs-detail', kwargs={'program_run_id': program_run_id})
        return JsonResponse({'redirect_url': url, 'data': data})
