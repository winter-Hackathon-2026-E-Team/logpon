from django.shortcuts import render, redirect
from django.views import View

from apps.timers.models import Timer
from apps.timers.forms.timer import TimerForm


class TimerDeleteView(View):
    template_name = "timers/timer_CRUD.html"

    def _build_rows(self):
        timers = Timer.objects.all().order_by("-id")
        rows = []
        for t in timers:
            form = TimerForm(instance=t, prefix=f"edit_{t.id}")
            rows.append({"timer": t, "form": form})
        return rows

    def post(self, request, id: int):
        deleted, _ = Timer.objects.filter(id=id).delete()

        if deleted:
            return redirect("timers:list")

        # 対象が無い（例：二重送信/別タブで削除済み）
        create_form = TimerForm(prefix="create")
        rows = self._build_rows()
        return render(
            request,
            self.template_name,
            {
                "create_form": create_form,
                "rows": rows,
                "delete_error": "削除対象のタイマーが見つかりませんでした",
                "open_delete_id": id,
            },
        )

    def get(self, request, id: int):
        return redirect("timers:list")


