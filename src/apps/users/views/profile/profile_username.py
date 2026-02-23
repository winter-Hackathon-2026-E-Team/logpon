from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ...models.users import User
from ...forms.profile.profile_username import ProfileUsernameForm

class ProfileUsernameView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = ProfileUsernameForm
    success_url = reverse_lazy('users:profile')
    success_message = 'ユーザ名の変更が完了しました'

    def form_invalid(self, form):
        return redirect('users:profile')
