from django.urls import path
from apps.timers.views.timer_list_create import TimerListCreateView
from apps.timers.views.timer_edit import TimerEditView
from apps.timers.views.timer_delete import TimerDeleteView

app_name = "timers"
urlpatterns = [
    path("", TimerListCreateView.as_view(), name="list"),  # GET:list / POST:create
    path("<int:id>/", TimerEditView.as_view(), name="edit"),  # GET:edit / POST:update
    path("<int:id>/delete/", TimerDeleteView.as_view(), name="delete"),  # POST:delete
]
