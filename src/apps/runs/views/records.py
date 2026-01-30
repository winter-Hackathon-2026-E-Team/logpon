from django.shortcuts import render, redirect
from django.views import View

class RecordsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'runs/records.html')

records = RecordsView.as_view()
