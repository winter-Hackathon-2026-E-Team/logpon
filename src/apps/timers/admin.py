from django.contrib import admin
from apps.timers.models import Sound, Timer


@admin.register(Sound)
class SoundAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "file_path", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(Timer)
class TimerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "duration_seconds", "sound", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("category", "is_active")
