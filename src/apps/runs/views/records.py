from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class RecordsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'runs/records.html')
