from django.urls import path
from apps.programs.views.program_timer import ProgramTimerCreateView
from apps.programs.views.program_timer import ProgramTimerDeleteView
from apps.programs.views.program_timer import ProgramTimerReorderView

app_name = "program_timers"

urlpatterns = [
    path("<int:program_id>/", ProgramTimerCreateView.as_view(), name="create"),
    path("<int:program_timer_id>/delete/", ProgramTimerDeleteView.as_view(), name="delete"),
    path("<int:program_id>/reorder/", ProgramTimerReorderView.as_view(), name="reorder"),
]
