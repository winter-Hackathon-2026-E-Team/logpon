# draft取得/作成（GET/POST）
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class ProgramDraftView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'runs/program-runs.html')
    
    def post(self, request, *args, **kwargs):
        pass
    