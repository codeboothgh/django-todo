from django.urls import path
from .views import *

app_name = "task"

urlpatterns = [
    # these are for function views
    # path("", index, name="home"),
    # path("create", create_task, name="create"),
    # path("<int:id>/", task_details, name="details"),
    # path("edit/<int:id>/", update_task, name="update"),
    # path("delete/<int:id>/", delete_task, name="delete"),
    # path("status/change/<int:id>/", change_status, name="change-status")

    # now, for class based views
    path("", TodoList.as_view(), name="home"),
    path("<int:id>/", TodoDetails.as_view(), name="details"),
    path("create/", CreateTodo.as_view(), name="create"),
    path("reaction/<int:todo_id>/<int:reaction>/", CreateTodoReaction.as_view(), name="reaction"),
    path("create-view/", CreateTodoView.as_view(), name="create-view")
]
