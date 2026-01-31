from django.urls import path

from .views import index, login, logout, password_reset, signup

app_name = 'users'
urlpatterns = [
    path('', index.IndexView.as_view(), name='index'),
    path('login/', login.UserLoginView.as_view(), name='login'),
    path('logout/', logout.UserLogoutView.as_view(), name='logout'),
    path('signup/', signup.SignupView.as_view(), name='signup'),
    path('password-reset/', password_reset.PasswordResetView.as_view(), name='password-reset')
]
