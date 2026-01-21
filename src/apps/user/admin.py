from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # 表示する列
    search_fields = ('name',)  # 検索対象
    list_filter = ('name',)  #
    
# Register your models here.
