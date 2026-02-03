from django.shortcuts import render, redirect
from django.views import View

from apps.timers.models import Timer
from apps.timers.forms.timer import TimerForm


class TimerEditView(View):
    template_name = "timers/timer_CRUD.html"

    def _build_rows(self, invalid_edit_id=None, invalid_edit_form=None):
        timers = Timer.objects.all().order_by("-id")
        rows = []
        for t in timers:
            if invalid_edit_id == t.id and invalid_edit_form is not None:
                form = invalid_edit_form
            else:
                form = TimerForm(instance=t, prefix=f"edit_{t.id}")
            rows.append({"timer": t, "form": form})
        return rows

    def post(self, request, id: int):
        timer = Timer.objects.filter(id=id).first()
        if timer is None:
            return redirect("timers:list")

        edit_form = TimerForm(request.POST, instance=timer, prefix=f"edit_{id}")
        if edit_form.is_valid():
            edit_form.save()
            return redirect("timers:list")

        # invalid：同じページに戻して、該当モーダルを自動で開く
        create_form = TimerForm(prefix="create")
        rows = self._build_rows(invalid_edit_id=id, invalid_edit_form=edit_form)
        return render(
            request,
            self.template_name,
            {"create_form": create_form, "rows": rows, "open_edit_id": id},
        )

    def get(self, request, id: int):
        return redirect("timers:list")

