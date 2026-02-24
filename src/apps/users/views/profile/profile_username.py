from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileUsernameView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pass
