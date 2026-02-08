from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from apps.programs.models import Program
from apps.programs.forms import ProgramForm


class ProgramListCreateView(LoginRequiredMixin, View):
    template_name = "programs/program_CRUD.html"
    login_url = "users:login"
    redirect_field_name = "next"
    
    def _build_rows(self, invalid_edit_id=None, invalid_edit_form=None):
        programs = Program.objects.filter(user=self.request.user).order_by("-id")
        rows = []
        for p in programs:
            if invalid_edit_id == p.id and invalid_edit_form is not None:
                form = invalid_edit_form
            else:
                form = ProgramForm(instance=p, prefix=f"edit_{p.id}")
            rows.append({"program": p, "form": form})
        return rows

    def get(self, request):
        create_form = ProgramForm(prefix="create")
        rows = self._build_rows()
        return render(request, self.template_name, {"create_form": create_form, "rows": rows})

    def post(self, request):
        create_form = ProgramForm(request.POST, prefix="create")
        if create_form.is_valid():
            program = create_form.save(commit=False)
            program.user = request.user  # ★ここが重要
            program.save()
            return redirect("programs:list")

        rows = self._build_rows()
        return render(request, self.template_name, {"create_form": create_form, "rows": rows})


