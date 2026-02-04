from django.shortcuts import render, redirect
from django.views import View

from apps.timers.models import Timer
from apps.timers.forms.timer import TimerForm
from apps.timers.views.mixins import TimerRowsMixin


class TimerEditView(TimerRowsMixin, View):
    template_name = "timers/timer_CRUD.html"

    def post(self, request, id: int):
        timer = Timer.objects.filter(id=id, is_active=True).first()
        if timer is None:
            return redirect("timers:list")

        edit_form = TimerForm(request.POST, instance=timer, prefix=f"edit_{id}")
        if edit_form.is_valid():
            edit_form.save()
            return redirect("timers:list")

        # invalid：同じページに戻して、該当モーダルを自動で開く
        create_form = TimerForm(prefix="create")
        rows = self.build_rows(invalid_edit_id=id, invalid_edit_form=edit_form)
        return render(
            request,
            self.template_name,
            {"create_form": create_form, "rows": rows, "open_edit_id": id},
        )

    def get(self, request, id: int):
        return redirect("timers:list")


