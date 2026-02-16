# /program-runs/<id>/ GET (実行画面)
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from ...selectors.program_runs import selector_exist_programs
from ...serializers.program_runs import serialize_exist_programs

class ProgramPagesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        programs = selector_exist_programs()
        context = serialize_exist_programs(programs)
        return render(request, 'runs/program-runs.html', context=context)
