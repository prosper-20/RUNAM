from django.urls import path
from .views import ViewAllTask, CreateNewTask

urlpatterns = [
    path("tasks/", ViewAllTask.as_view(), name="all-taks"),
    path("tasks/create/", CreateNewTask.as_view(), name="create"),
]