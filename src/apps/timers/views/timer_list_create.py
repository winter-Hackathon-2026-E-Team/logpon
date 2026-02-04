from django.shortcuts import render, redirect
from django.views import View

from apps.timers.forms.timer import TimerForm
from apps.timers.views.mixins import TimerRowsMixin


class TimerListCreateView(TimerRowsMixin, View):
    template_name = "timers/timer_CRUD.html"  # テンプレートは後で変える

    def get(self, request):
        create_form = TimerForm(prefix="create")
        rows = self.build_rows()
        return render(request, self.template_name, {"create_form": create_form, "rows": rows})

    def post(self, request):
        create_form = TimerForm(request.POST, prefix="create")
        if create_form.is_valid():
            create_form.save()
            return redirect("timers:list")

        rows = self.build_rows()
        return render(request, self.template_name, {"create_form": create_form, "rows": rows})





