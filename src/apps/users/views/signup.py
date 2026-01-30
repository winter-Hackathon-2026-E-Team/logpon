from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from ..forms.signup import SignUpForm

# Create your views here.
class SignupView(CreateView):
    template_name = 'users/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('users:login')
    
    def form_valid(self, form):
        return super().form_valid(form) # success_urlにレスポンス

signup = SignupView.as_view()
