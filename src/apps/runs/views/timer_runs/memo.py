import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.runs.models import TimerRun  # パスは合わせて

class TimerRunsMemoView(LoginRequiredMixin, View):
    def post(self, request, timer_run_id: int):
        run = get_object_or_404(TimerRun, id=timer_run_id, user=request.user)  # 所有者チェック

        # JSON / form どちらでも受ける
        ct = request.headers.get("Content-Type", "")
        if ct.startswith("application/json"):
            try:
                payload = json.loads(request.body.decode("utf-8") or "{}")
            except json.JSONDecodeError:
                return JsonResponse({"error": "JSONが不正です"}, status=400)
            memo = (payload.get("memo") or "").strip()
        else:
            memo = (request.POST.get("memo") or "").strip()

        # バリデーション（必要なら）
        if len(memo) > 5000:
            return JsonResponse({"error": "メモが長すぎます"}, status=400)

        run.memo = memo
        run.save(update_fields=["memo"])

        return JsonResponse({"ok": True, "memo": run.memo})

