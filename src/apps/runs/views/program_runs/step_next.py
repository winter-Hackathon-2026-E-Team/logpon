# プログラムのnext（自動遷移）（POST）
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class ProgramNextView(LoginRequiredMixin, View):
    def post(self, request, program_run_id):
        if not request.body:
            return JsonResponse({'error': 'リクエストボディが空です'}, status=400)
        try:
            body = json.loads(request.body)
            timer_run_id = body.get('timer_run_id')
            elapsed_sec = int(body.get('elapsed_sec'))
            status_next(program_run_id, timer_run_id, elapsed_sec)
            program_run, timer_run = selector_pause_programRun_timerRun(program_run_id, timer_run_id)
            runs_data = serialize_pause_runs(program_run, timer_run)
            return JsonResponse({'runs_data': runs_data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
