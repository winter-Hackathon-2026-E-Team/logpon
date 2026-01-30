from django.shortcuts import render, redirect
from django.views import View
from ..forms.signup import SignUpForm

# Create your views here.
class SignupView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/signup.html')

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'users/login.html')
        else:
            return render(request, 'users/signup.html')

signup = SignupView.as_view()
