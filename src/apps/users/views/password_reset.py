from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse

# Create your views here.
class PasswordResetView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/password-reset.html')

    def post(self, request, *args, **kwargs):
        pass

password_reset = PasswordResetView.as_view()
