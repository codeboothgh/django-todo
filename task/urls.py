from django.urls import path
from .views import *

app_name = "task"

urlpatterns = [
    path("", index, name="home"),
    path("create", create_task, name="create"),
    path("<int:id>/", task_details, name="details"),
    path("edit/<int:id>/", update_task, name="update"),
    path("delete/<int:id>/", delete_task, name="delete"),
    path("status/change/<int:id>/", change_status, name="change-status")
]
