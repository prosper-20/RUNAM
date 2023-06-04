from django.urls import path
from .views import ViewAllTask

urlpatterns = [
    path("tasks/", ViewAllTask.as_view(), name="all-taks")
]