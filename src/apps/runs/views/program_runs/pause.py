# プログラムのpause（一時停止）（POST）
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class ProgramPauseView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pass
