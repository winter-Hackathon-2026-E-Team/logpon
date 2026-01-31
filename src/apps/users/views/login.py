import logging
from django.contrib import messages
from django.contrib.auth.views import LoginView
from ..forms.login import LoginForm

logger = logging.getLogger(__name__)

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        messages.success(self.request, 'ログインしました。')
        logger.info("[login] SUCCESS user_id=%s email=%s", getattr(user, "id", None), getattr(user, "email", None))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'メールアドレスまたはパスワードが違います。')
        logger.warning(
            "[login] FAILED username=%s non_field=%s errors=%s",
            form.data.get("username"),
            list(form.non_field_errors()),
            dict(form.errors),
        )
        return super().form_invalid(form)
