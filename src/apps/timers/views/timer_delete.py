from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.timers.models import Timer
from apps.timers.forms.timer import TimerForm
from apps.timers.views.mixins import TimerRowsMixin

class TimerDeleteView(LoginRequiredMixin, TimerRowsMixin, View):
    template_name = "timers/timer_CRUD.html"

    def post(self, request, id: int):
        deleted, _ = Timer.objects.filter(id=id, user=request.user).delete()

        if deleted:
            return redirect("timers:list")

        create_form = TimerForm(prefix="create")
        rows = self.build_rows(user=request.user)
        return render(request, self.template_name, {
            "create_form": create_form,
            "rows": rows,
            "delete_error": "削除対象のタイマーが見つかりませんでした",
            "open_delete_id": id,
        })


    def get(self, request, id: int):
        return redirect("timers:list")

