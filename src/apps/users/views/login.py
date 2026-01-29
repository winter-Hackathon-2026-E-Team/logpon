from django.shortcuts import render, redirect
from django.views import View
from ..forms.login import LoginForm

# Create your views here.
class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/login.html')

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        is_valid = form.is_valid()

        if not is_valid:
            return render(request, 'users/login.html', {'form': form})
        
        pass

login = LoginView.as_view()
