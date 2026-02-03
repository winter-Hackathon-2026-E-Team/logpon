from django.shortcuts import render, redirect
from django.views import View

from apps.timers.models import Timer
from apps.timers.forms.timer import TimerForm


class TimerListCreateView(View):
    template_name = "timers/timer_CRUD.html" # テンプレートは後で変える

    def _build_rows(self, invalid_edit_id=None, invalid_edit_form=None):
        #テンプレで (timer, form) を一緒に回せる形にする
        timers = Timer.objects.all().order_by("-id")
        rows = []
        for t in timers:
            if invalid_edit_id == t.id and invalid_edit_form is not None:
                form = invalid_edit_form
            else:
                form = TimerForm(instance=t, prefix=f"edit_{t.id}")
            rows.append({"timer": t, "form": form})
        return rows

    def get(self, request):
        create_form = TimerForm(prefix="create")
        rows = self._build_rows()
        return render(request, self.template_name, {"create_form": create_form, "rows": rows})

    def post(self, request):
        create_form = TimerForm(request.POST, prefix="create")
        if create_form.is_valid():
            create_form.save()
            return redirect("timers:list")

        # invalidの場合は同じ画面にエラー付きで表示
        rows = self._build_rows()
        return render(request, self.template_name, {"create_form": create_form, "rows": rows})




