# プログラムのpause（一時停止）（POST）
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class ProgramPauseView(LoginRequiredMixin, View):
    def post(self, request, program_run_id):
        return JsonResponse({'runs_data': 'aaa'})
