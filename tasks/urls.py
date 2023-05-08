from django.urls import path
from .views import (
    TaskView,
    ApiTaskView,
    AcceptTaskView,
    ApiCompletedTasksView,
    ApiAvailableTasksView,
    ApiUndergoingTaskView,
    ApiEditTaskView,
    ApiTaskHistory,
    ApiTaskReview,
    ApiTaskBidView, 
    ApiTaskRequestView,
    ApiTaskErrandSerializer,
    ApiMyTotalEarningView,

)

urlpatterns = [
    path("", ApiTaskView.as_view(), name="task"),
    path("my-requests/", ApiTaskRequestView.as_view(), name="requested-tasks"),
    path("my-errands/", ApiTaskErrandSerializer.as_view(), name="errands"),
    path("my-earnings/", ApiMyTotalEarningView.as_view(), name="my-earnings"),
    path("history/",  ApiTaskHistory.as_view(), name="tasks-history"),
    path("accept/", AcceptTaskView.as_view(), name="accept-task"),
    path("available/", ApiAvailableTasksView.as_view(), name="available-tasks"),
    path("running/", ApiUndergoingTaskView.as_view(), name="running-tasks"),
    path("completed/", ApiCompletedTasksView.as_view(), name="completed-tasks"),
    path("<str:id>/reviews/", ApiTaskReview.as_view(), name="task-review"),
    path("<str:id>/bid/", ApiTaskBidView.as_view(), name="task-bid-create"),
    path("<str:id>/", ApiEditTaskView.as_view(), name="task-detail"),
    
    
    
    
    
]