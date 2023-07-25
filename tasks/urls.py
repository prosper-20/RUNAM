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
    ApiNewBidderView,
    ApiMyPerformanceView,
    ApiMyActivityView,
    ApiTaskAssignmentView,
    ApiPostTaskAssignmentView,
    ApiTaskSupport,
    APITaskShopView,
    ApiCreateTaskShopView,
    ApiTaskShopDetailView,
    ApiCreateTaskShopSubscriber,
    ApiShopCreateTaskView

)

urlpatterns = [
    path("", ApiTaskView.as_view(), name="task"),
    path("<str:id>/new-bidder/", ApiNewBidderView.as_view(), name="new_bidder"),
    path("my-requests/", ApiTaskRequestView.as_view(), name="requested-tasks"),
    path("my-activity/", ApiMyActivityView.as_view(), name="my-activity"),
    path("my-errands/", ApiTaskErrandSerializer.as_view(), name="errands"),
    path("my-earnings/", ApiMyTotalEarningView.as_view(), name="my-earnings"),
    path("my-performace/", ApiMyPerformanceView.as_view(), name="my-performance"),
    # URLS FOR SHOP
    path("shops/all/", APITaskShopView.as_view(), name="tasks-shop"),
    path("shop/create/", ApiCreateTaskShopView.as_view(), name="create-shop"),
    path("shop/<slug:slug>/subscribe/", ApiCreateTaskShopSubscriber.as_view(), name="shop-sunscriber"),
    path("shop/<slug:slug>/create-task/", ApiShopCreateTaskView.as_view(), name="create-shop-task"),
    path("shop/<slug:slug>/", ApiTaskShopDetailView.as_view(), name="shop-detail"),
    #  URLS FOR TASK
    path("history/",  ApiTaskHistory.as_view(), name="tasks-history"),
    path("accept/", AcceptTaskView.as_view(), name="accept-task"),
    path("available/", ApiAvailableTasksView.as_view(), name="available-tasks"),
    path("running/", ApiUndergoingTaskView.as_view(), name="running-tasks"),
    path("completed/", ApiCompletedTasksView.as_view(), name="completed-tasks"),
    path("<str:id>/reviews/", ApiTaskReview.as_view(), name="task-review"),
    path("<str:id>/bid/", ApiTaskBidView.as_view(), name="task-bid-create"),
    path("<str:id>/bidders/", ApiTaskAssignmentView.as_view(), name="task-bidders"),
    path("<str:id>/contact-support/", ApiTaskSupport.as_view(), name="contact-support"),
    path("<str:id>/bidders/assign/<str:username>/", ApiPostTaskAssignmentView.as_view(), name="task-assign-bidder"),
    path("<uuid:id>/", ApiEditTaskView.as_view(), name="task-detail"),
    
    
]