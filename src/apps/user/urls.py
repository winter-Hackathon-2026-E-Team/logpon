from django.urls import path
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    # テスト用index
    path('index/', views.index, name='index'),
    # 管理者サインアップ/ログイン
    path('signup/', views.signup, name='signup'),
    path('login/', views.admin_login, name='admin_login'),


]