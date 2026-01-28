from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

class User(AbstractUser):
    class Meta:
        db_table = 'users'
    
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(max_length=255, validators=[username_validator],)
    password = models.CharField(max_length=255,)
    email = models.EmailField(blank=False, unique=True,)
    # is_staff, is_activeはAbstractUserより継承
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True,)

    USERNAME_FIELD = 'email' # このテーブルのレコードを一意に識別
    REQUIRED_FIELDS = ['username'] # スーパーユーザー作成時に入力する

    def __str__(self) -> str:
        return self.email
