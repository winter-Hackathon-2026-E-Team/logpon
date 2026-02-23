from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ...models.users import User
from ...forms.profile.profile_email import ProfileEmailForm

class ProfileEmailView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = ProfileEmailForm
    success_url = reverse_lazy('users:profile')
    success_message = 'emailの変更が完了しました'

    def form_invalid(self, form):
        return redirect('users:profile')

