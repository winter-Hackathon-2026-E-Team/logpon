from __future__ import annotations

from collections import defaultdict
from datetime import datetime, time, timedelta, date as date_type

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views import View

from apps.runs.models import ProgramRun, TimerRun  


def _iso(dt):
    return dt.isoformat() if dt else None


def _safe_int(v, default=0) -> int:
    try:
        return int(v)
    except Exception:
        return default


class RecordsView(LoginRequiredMixin, View):
    
    template_name = "runs/records.html"
    login_url = "users:login"
    redirect_field_name = "next"

    def get(self, request):
        return render(request, self.template_name)


class RecordsDataView(LoginRequiredMixin, View):
   
    login_url = "users:login"
    redirect_field_name = "next"

    def get(self, request):
        # date クエリ（無ければ今日）
        q = (request.GET.get("date") or "").strip()
        target_date: date_type | None = parse_date(q) if q else None
        if target_date is None:
            target_date = timezone.localdate()

        # その日の [00:00, 24:00) 範囲を作る（TIME_ZONE基準）
        tz = timezone.get_current_timezone()
        range_from = timezone.make_aware(datetime.combine(target_date, time.min), tz)
        range_to = range_from + timedelta(days=1)

        # ProgramRun: started_at で当日分を抽出
        pr_qs = (
            ProgramRun.objects
            .filter(user=request.user, started_at__gte=range_from, started_at__lt=range_to)
            .order_by("-started_at", "-id")
        )

        program_runs = list(pr_qs)

        if not program_runs:
            return JsonResponse({
                "date": target_date.isoformat(),
                "programs": [],
                "timer_runs": [],
                "daily_total_elapsed_sec": 0,
            })

        program_run_ids = [pr.id for pr in program_runs]

        # TimerRun: 当日の ProgramRun に紐づく全件
        tr_qs = (
            TimerRun.objects
            .filter(program_run_id__in=program_run_ids)
            .select_related("program_run")
            .order_by("program_run_id", "id")
        )

        timer_runs_list = list(tr_qs)

        # programごとの合計秒 & 日合計秒（TimerRun.elapsed_sec から算出）
        totals_by_program = defaultdict(int)
        daily_total = 0
        for tr in timer_runs_list:
            sec = _safe_int(getattr(tr, "elapsed_sec", 0) or 0)
            totals_by_program[tr.program_run_id] += sec
            daily_total += sec

       
        programs = []
        for pr in program_runs:
            program_name = (
                getattr(pr, "program_name_snapshot", None)
                or getattr(pr, "program_name", None)
                or "（no name）"
            )

            programs.append({
                "program_run_id": pr.id,
                "program_name": program_name,
                "total_elapsed_sec": totals_by_program.get(pr.id, 0),
                "updated_at": _iso(getattr(pr, "updated_at", None))
                              or _iso(getattr(pr, "ended_at", None))
                              or _iso(getattr(pr, "started_at", None)),
            })

        # フロント互換：started_at を runninged_at キーで返す
        timer_runs = []
        for tr in timer_runs_list:
            timer_name = (
                getattr(tr, "timer_name_snapshot", None)
                or getattr(tr, "timer_name", None)
                or "（no name）"
            )

            started = getattr(tr, "started_at", None)
            ended = getattr(tr, "ended_at", None)

            timer_runs.append({
                "program_run_id": tr.program_run_id,
                "timer_run_id": tr.id,
                "timer_name": timer_name,
                "runninged_at": _iso(started),  # 互換キー
                "ended_at": _iso(ended),
                "updated_at": _iso(getattr(tr, "updated_at", None)) or _iso(ended) or _iso(started),
                "elapsed_sec": _safe_int(getattr(tr, "elapsed_sec", 0) or 0),
                "memo": getattr(tr, "memo", None),
            })

        return JsonResponse({
            "date": target_date.isoformat(),
            "programs": programs,
            "timer_runs": timer_runs,
            "daily_total_elapsed_sec": int(daily_total),
        })


