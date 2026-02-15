# プログラムのresume（再開）（POST）
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class ProgramResumeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pass
