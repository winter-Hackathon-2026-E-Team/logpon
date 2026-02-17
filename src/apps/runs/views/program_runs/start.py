# プログラムのstart（初期実行）（POST）
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class ProgramStartView(LoginRequiredMixin, View):
    def post(self, request, program_run_id):
        data = json.loads(request.body)
        
        return JsonResponse({'runs_data': 'aaa'})

