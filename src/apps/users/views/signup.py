from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse

# Create your views here.
class SignupView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<html lang="ja"><body><h1>signup_view</h1></body></html>')

    def post(self, request, *args, **kwargs):
        pass

signup = SignupView.as_view()
