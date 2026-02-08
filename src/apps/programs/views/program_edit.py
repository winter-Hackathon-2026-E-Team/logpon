from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.views import View

from apps.programs.models import Program
from apps.programs.forms import ProgramForm


class ProgramEditView(LoginRequiredMixin, View):
    template_name = "programs/program_CRUD.html"
    login_url = "users:login"
    redirect_field_name = "next"
    
    def get(self, request, program_id):
        return redirect("programs:list")  # 1画面運用

    def post(self, request, program_id):
        program = get_object_or_404(Program, id=program_id, user=request.user)  # ★自分のだけ
        form = ProgramForm(request.POST, instance=program, prefix=f"edit_{program_id}")

        if form.is_valid():
            form.save()
            return redirect("programs:list")

        # エラー時：同じ画面に該当行だけエラー付きで返す
        create_form = ProgramForm(prefix="create")
        programs = Program.objects.filter(user=request.user).order_by("-id")
        rows = []
        for p in programs:
            rows.append({
                "program": p,
                "form": form if p.id == program_id else ProgramForm(instance=p, prefix=f"edit_{p.id}"),
            })
        return render(request, self.template_name, {"create_form": create_form, "rows": rows})

