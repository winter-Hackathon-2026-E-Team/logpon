from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.timers.forms.timer import TimerForm
from apps.timers.views.mixins import TimerRowsMixin


class TimerListCreateView(LoginRequiredMixin, TimerRowsMixin, View):
    template_name = "timers/timer_CRUD.html"
    login_url = "users:login"          # URL name に合わせる（または "/login/"）
    redirect_field_name = "next" # デフォルトでOK

    def get(self, request):
        create_form = TimerForm(prefix="create")
        rows = self.build_rows(user=request.user)
        return render(request, self.template_name, {"create_form": create_form, "rows": rows})

    def post(self, request):
        create_form = TimerForm(request.POST, prefix="create")
        if create_form.is_valid():
            create_form.save(user=request.user)
            return redirect("timers:list")

        rows = self.build_rows(user=request.user)
        return render(request, self.template_name, {"create_form": create_form, "rows": rows})






