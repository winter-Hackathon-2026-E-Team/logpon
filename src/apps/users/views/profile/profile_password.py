from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfilePasswordView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    success_url = reverse_lazy('users:profile')
    success_message = 'パスワードの変更が完了しました'

    def form_invalid(self, form):
        messages.error(self.request, 'エラー')
        return redirect('users:profile')