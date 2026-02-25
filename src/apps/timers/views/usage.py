from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.timers.models import Timer
from apps.programs.models import ProgramTimer


class TimerUsageView(LoginRequiredMixin, View):
    def get(self, request, timer_id: int):
        timer = get_object_or_404(Timer, id=timer_id, user=request.user)

        qs = (
            ProgramTimer.objects
            .select_related("program")
            .filter(timer=timer, program__user=request.user)
            .order_by("-id")
        )

        used_count = qs.count()

        # 先頭3件のプログラム名
        pts = list(qs[:3])
        program_names = []
        for pt in pts:
            p = pt.program
            name = getattr(p, "program_name", None) or getattr(p, "name", None) or str(p)
            program_names.append(name)

        remain_count = max(used_count - len(program_names), 0)

        return JsonResponse({
            "used_count": used_count,
            "program_names": program_names,
            "remain_count": remain_count,
        })