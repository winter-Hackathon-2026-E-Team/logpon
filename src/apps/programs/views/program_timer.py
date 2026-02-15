from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.programs.models import Program, ProgramTimer
from apps.programs.services.program_timer import (
    add_timer_to_program,
    delete_program_timer,
    reorder_program_timers,
)
from apps.timers.models import Timer


class ProgramTimerCreateView(LoginRequiredMixin, View):
    def post(self, request, program_id: int):
        program = get_object_or_404(Program, id=program_id, user=request.user)

        timer_id = (request.POST.get("timer_id") or "").strip()
        if not timer_id.isdigit():
            messages.error(request, "タイマーが不正です")
            return redirect("programs:list")

        timer = get_object_or_404(Timer, id=int(timer_id), user=request.user)

        add_timer_to_program(program=program, timer=timer)
        messages.success(request, "タイマーを追加しました")
        return redirect("programs:list")


class ProgramTimerDeleteView(LoginRequiredMixin, View):
    def post(self, request, program_timer_id: int):
        pt = get_object_or_404(
            ProgramTimer,
            id=program_timer_id,
            program__user=request.user,
        )
        delete_program_timer(program_timer=pt)
        messages.success(request, "タイマーを削除しました")
        return redirect("programs:list")


class ProgramTimerReorderView(LoginRequiredMixin, View):
    def post(self, request, program_id: int):
        program = get_object_or_404(Program, id=program_id, user=request.user)

        order_str = (request.POST.get("order") or "").strip()  # "12,9,10"
        try:
            ordered_ids = [int(x) for x in order_str.split(",") if x.strip()]
        except ValueError:
            messages.error(request, "並び替えデータが不正です")
            return redirect("programs:list")

        try:
            reorder_program_timers(program=program, ordered_ids=ordered_ids)
        except ValueError:
            messages.error(request, "並び替え対象が一致しません（再読み込みしてやり直してください）")
            return redirect("programs:list")

        messages.success(request, "並び順を保存しました")
        return redirect("programs:list")
