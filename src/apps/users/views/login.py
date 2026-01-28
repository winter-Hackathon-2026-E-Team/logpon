from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse

# Create your views here.
class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/login.html')

    def post(self, request, *args, **kwargs):
        pass

login = LoginView.as_view()
