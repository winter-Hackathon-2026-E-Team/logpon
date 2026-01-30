from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from ..forms.signup import SignUpForm
import logging

logger = logging.getLogger(__name__)


class SignupView(CreateView, SuccessMessageMixin):
    template_name = 'users/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('users:login')
    success_message = '新規登録が完了しました。ログインしてください。'

    def dispatch(self, request, *args, **kwargs):
        logger.warning("SignupView dispatch: method=%s path=%s", request.method, request.path)
        return super().dispatch(request, *args, **kwargs)
    
    def form_invalid(self, form):
        logger.warning("Signup invalid. errors=%s", form.errors)
        logger.warning("POST=%s", self.request.POST)
        messages.error(self.request, '入力内容にエラーがあります。')
        response = super().form_invalid(form)
        return response

    def form_valid(self, form):
        logger.warning("Signup valid. cleaned_data=%s", form.cleaned_data)
        response = super().form_valid(form)
        logger.warning("Created user pk=%s email=%s", self.object.pk, self.object.email)
        return response # success_urlにレスポンス

signup = SignupView.as_view()
