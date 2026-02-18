import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.runs.models import TimerRun


class TimerRunsMemoView(LoginRequiredMixin, View):
    def post(self, request, timer_run_id: int):
        run = get_object_or_404(
            TimerRun.objects.select_related("program_run"),
            id=timer_run_id,
            program_run__user=request.user,
        )

        ct = request.headers.get("Content-Type", "")
        if ct.startswith("application/json"):
            try:
                payload = json.loads(request.body.decode("utf-8") or "{}")
            except json.JSONDecodeError:
                return JsonResponse({"error": "JSONが不正です"}, status=400)
            memo = (payload.get("memo") or "").strip()
        else:
            memo = (request.POST.get("memo") or "").strip()

        # validation
        if len(memo) > 5000:
            return JsonResponse({"error": "メモが長すぎます"}, status=400)

        run.memo = memo

        run.save(update_fields=["memo"])

        updated_at = getattr(run, "updated_at", None)
        return JsonResponse({
            "timer_run_id": run.id,
            "memo": run.memo,
            "updated_at": updated_at.isoformat() if updated_at else None,
        })


