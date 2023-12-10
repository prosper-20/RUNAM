from django.shortcuts import render, get_object_or_404
from rest_framework import serializers
from .models import Task, AcceptTask, TaskReview, Bidder, NewBidder, Support, Shop, LabReportTask, LaundryTask,  Commission
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views import View
from decimal import Decimal
from .serializers import (
    LaundryTaskSerializer,
    LabReportSerializer,
    TaskSerializer, 
    AcceptTaskSerializer, 
    TaskReviewSerializer, 
    GetBidderSerializer, 
    PostBidderSerializer, 
    TaskRequestSerializer, 
    MyTotalEarningsSerializer, 
    TaskDetailSerializer, 
    ChangePasswordSerializer, 
    PostNewBidderSerializer, 
    GetNewBidderSerializer, 
    TaskSupportSerializer, 
    ShopSerializer,
    CreateShopTaskSerializer)
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
from users.models import CustomUser
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import HasPhoneNumberPermission
from accounts.models import User as Accounts_user
from django.http import HttpResponse
import json
from geolocation import get_ip_geolocation_data

class APITaskShopView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ShopSerializer

    def get(self, request, format=None):
        all_shops = Shop.objects.all()
        serializer = ShopSerializer(all_shops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ApiTaskShopDetailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ShopSerializer

    def get(self, request, slug, format=None):
        try:
            shop = Shop.objects.get(slug=slug)
        except Shop.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ShopSerializer(shop)
        new = dict(serializer.data)
        user = request.user
        if user not in shop.subscribers.all():
            return Response({
            "name": new["name"],
            "slug": new["slug"],
            "tasks": new["tasks"],
            "description": new["description"],
            "tasks": new["tasks"],
            "rating": new["rating"],
            "subscribe": f"http://127.0.0.1:8000/shop/{slug}/subscribe/"}, status=status.HTTP_200_OK)
        elif user == shop.owner:
            return Response({
            "name": new["name"],
            "slug": new["slug"],
            "tasks": new["tasks"],
            "description": new["description"],
            "tasks": new["tasks"],
            "subscribers": new["subscribers"],
            "rating": new["rating"],
        })

        return Response({
            "name": new["name"],
            "slug": new["slug"],
            "tasks": new["tasks"],
            "description": new["description"],
            "tasks": new["tasks"],
            "rating": new["rating"],
        })
        
    
        # return Response(serializer.data, status=status.HTTP_200_OK)
    
    

    def put(self, request, slug, format=None):
        try:
            shop = Shop.objects.get(slug=slug)
        except Shop.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ShopSerializer(shop, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request, slug, format=None):
        shop = Shop.objects.get(slug=slug)
        user = request.user
        if user != shop.owner:
            return Response({"Error": "You do not have the permission to perform this action"})
        shop.delete()
        return Response({"Success": "Post delete successful"}, status=status.HTTP_204_NO_CONTENT)


    

class ApiCreateTaskShopView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShopSerializer

    def post(self, request, format=None):
        user = request.user
        new_shop = Shop(owner=user)
        serializer = ShopSerializer(new_shop, data=request.data)
        serializer.is_valid(raise_exception=True)
        new_shop = serializer.save()
        print(new_shop)
        return Response({
            "Sucess": "Your virtual shop has been created, kindly upload supporting" 
            " business documents to enable you upload tasks...Documents include: CAC Certificate, Certificate of Incorporation etc",
            "name": new_shop.name,
            "owner": new_shop.owner.username,
            "description": new_shop.description,
            "location": new_shop.location
        }, status=status.HTTP_201_CREATED)


class ApiCreateTaskShopSubscriber(APIView):
    permission_classes = [IsAuthenticated]
    '''
    This view enables users to subscribe to a shop
    for tasks.
    '''
    def post(self, request, slug, format=None):
        current_shop = Shop.objects.get(slug=slug)
        user = request.user
        current_shop.subscribers.add(user)
        return Response({"Success": f"Thnak you for subscribing to {current_shop.name}"})
    

class ApiShopCreateTaskView(APIView):
    permission_classes = [IsAuthenticated]
    '''
    This view allows shop owners to create tasks
    that'll be visible to other RUNAM users
    '''
    def post(self, request, slug, format=None):
        current_shop = Shop.objects.get(slug=slug)
        current_user = request.user
        if current_shop.owner != current_user:
            return Response({"Error": "You don't have the permission to performm this action"}, status=status.HTTP_401_UNAUTHORIZED)
        elif current_shop.is_verified == False:
            return Response({"Error": "You cannot post a task until you complete your shop profile",
                             "link": "complete_profile_link"}, status=status.HTTP_401_UNAUTHORIZED)
        
        new_shop_task = Task(shop=current_shop, sender=current_shop.owner)
        serializer = CreateShopTaskSerializer(new_shop_task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
     



    

class TaskView(APIView):
    # permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #     """Returns Polls that were created today"""
    #     return Task.objects.exclude(sender=self.request.user.pk)

    
    
    def get(self, request, format=None):
        # queryset = Task.objects.filter(is_active=False)
        queryset = Task.objects.exclude(sender=self.request.user) | Task.objects.exclude(picked_up=True)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data, request.user,  status=status.HTTP_200_OK)
    
    
    def post(self, request, format=None):
        data = request.data
        data['sender'] = request.user.pk
        serializer =TaskSerializer(data=data)
        data = {}
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        data["Success"] = "Task has been created"
        data["id"] = task.id
        data["name"] = task.name
        data["description"] = task.description
        # data["sender"] = task.sender
        data["completed"] = task.completed

        return Response(data=data, status=status.HTTP_201_CREATED)



class Home(View):
    def get(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        geolocation_json = get_ip_geolocation_data(ip)
        geolocation_data = json.loads(geolocation_json)
        print(geolocation_data)
        country = geolocation_data['country']
        region = geolocation_data['region']
        return HttpResponse("Welcome! Your IP address is: {} and you are visiting from {} in {}".format(ip, region, country))


class ApiTaskView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # permission_classes = [IsAuthenticated, HasPhoneNumberPermission]
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("name", "sender__username", "category__name", "description")

    def embed(self, request,*args, **kwargs):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return HttpResponse("Welcome! You are visiting from: {}".format(ip))
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  # Specify your desired permission class for GET requests
        elif self.request.method == 'POST':
            return [IsAuthenticated(), HasPhoneNumberPermission()]  # Specify your desired permission class for POST requests
        return []


    def get_context_data(self, request, **kwargs):
        # Call the base implementation first to get a context
        context = super(ApiTaskView, self).get_context_data(**kwargs)
        context={'request': request}
        return context

    def perform_create(self, serializer):
        user = self.request.user
        account = Accounts_user.objects.get(email=user)
        print(account)
        print(user)
        # serializer.save(sender=self.request.user)
        serializer.save(sender=account)
        return super().perform_create(serializer)
    


    
# class ApiEditTaskView(RetrieveUpdateDestroyAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer


class ApiEditTaskView(APIView):
    # permission_classes = [IsAuthenticated,]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  # Specify your desired permission class for GET requests
        elif self.request.method == 'PUT':
            return [IsAuthenticated()]  # Specify your desired permission class for POST requests
        return []
    
    def get(self, request, id, format=None):
        try: 
            task = Task.objects.get(id=id)
            serializer = TaskDetailSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({"Error": "Cannot find a matching task"})
        
    
    def put(self, request, id, format=None):
        serializer_context = {
            'request': request,
        }
        try: 
            task = Task.objects.get(id=id)
            if request.user == task.sender:
                serializer = TaskSerializer(task, data=request.data, context=serializer_context, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"Error": "You cannot edit someone else's task"}, status=status.HTTP_401_UNAUTHORIZED)
        except Task.DoesNotExist:
            return Response({"Error": "Cannot find a matching task"})
        
    
    def delete(self, request, id, format=None):
        try: 
            task = Task.objects.get(id=id)
            if request.user == task.sender:
                task.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"Error": "You cannot delete someone else's task"}, status=status.HTTP_401_UNAUTHORIZED)
        except Task.DoesNotExist:
            return Response({"Error": "Cannot find a matching task"})
        
 


class ApiAvailableTasksView(APIView): #You changed this from ListAPIView to APIView
    def get(self, request, format=None):
        queryset = Task.objects.exclude(sender=self.request.user)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        


class ApiUndergoingTaskView(ListAPIView):
    queryset = Task.objects.filter(picked_up=True)
    serializer_class = TaskSerializer


class ApiCompletedTasksView(ListAPIView):
    queryset = Task.objects.filter(completed=True)
    serializer_class = TaskSerializer


    


class AcceptTaskView(APIView): 
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        serializer = AcceptTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        get_task = serializer.data.get("task")
        print("prosper", get_task)
        sender_pk = Task.objects.get(id=get_task).sender
        print("edward", sender_pk)
        # print("edward", task_sender_pk)
        # get_sender_pk = User.objects.get(get_task.sender)
        # user = serializer.data.get("receiver")
        # if get_sender_pk == user:
        #     return Response({"Error": "You cannot assign a task to yourself"})
        user = serializer.data.get("receiver")
        receiver_pk = CustomUser.objects.get(pk=user)
        if sender_pk == receiver_pk:
            return Response({"Error": "You cant assign a task to yourself"})
        task_id = serializer.data.get("task")
        task = Task.objects.get(id=task_id)
        task.is_active = False
        task.picked_up = True
        task.save()
        username = CustomUser.objects.get(pk=user).username
        print(username)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    



class ApiTaskHistory(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self, request, format=None):
        tasks = Task.objects.filter(sender=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    


class ApiTaskReview(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = TaskReviewSerializer

   

    def get(self, request, id, format=None):
        try:
            print("request", request)
            current_task = Task.objects.get(id=id)
            all_task_reviews = TaskReview.objects.filter(task=id)
            print(current_task)
            print(all_task_reviews.count())
        except Task.DoesNotExist:
            return Response({"Error": "Can't find a matching task"}, status=status.HTTP_404_NOT_FOUND)
        
        if all_task_reviews.count() == 0:
            return Response({"No reviews yet": "0",
                             "Add one": f"http://127.0.0.1:8000/tasks/{id}/reviews/"})
        
        serializer = TaskReviewSerializer(all_task_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request, id, format=None):
        try:
            task = Task.objects.get(id=id)
            if task.completed == False:
                return Response({"Error": "You cannot review a task that has not been completed"})
            elif request.user != task.sender or request.user != task.messenger:
                return Response({"Error": "You don't have the permission to review this task!!"}, status=status.HTTP_403_FORBIDDEN)
        except Task.DoesNotExist:
            return Response({"Error": "Can't find a matching task"})
        
        review = TaskReview(task=task, errander=request.user)
        serializer = TaskReviewSerializer(review, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    


# class ApiCreateTaskBidView(APIView):
#     def put(self, request, id, format=None):
#         task = Task.objects.get(id=id)


class ApiTaskBidView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, id, format=None):
        task = Task.objects.get(id=id)
        bidders = Bidder.objects.filter(task=task.id)
        serializer = GetBidderSerializer(bidders, many=True)
        print(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    
    def post(self, request, id, format=None):
        task_id = Task.objects.get(id=id).id
        task = Task.objects.get(id=id)
        user = request.user
        account = Accounts_user.objects.get(email=user)
        print(task)
        print(task.id)
        print(user)
        if task.sender == account:
            return Response({"Error": "You cannot bid for a task you created"}, status=status.HTTP_400_BAD_REQUEST)
        
        if Bidder.objects.filter(task=task.id, user=user).exists():
            return Response({
                    "Error": "You can not bid twice for a task"
                 }, status=status.HTTP_400_BAD_REQUEST)

        new_bidder = Bidder(task=task, user=account)
        
        serializer = PostBidderSerializer(new_bidder, data=request.data)
        serializer.is_valid(raise_exception=True)
        new_bidder_data = serializer.save()
        task.task_bidders.add(new_bidder)
        task.save()
        return Response(
            {"Success": "Bid for task submitted",
            "user": user.profile.username,
            "message": new_bidder_data.message
                        } ,status=status.HTTP_201_CREATED)

        
    def put(self, request, id, format=None):
        task = Task.objects.get(id=id)
        user = request.user
        account = Accounts_user.objects.get(email=user)
        try:
            bid = Bidder.objects.get(task=task, user=account)
        except Bidder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = PostBidderSerializer(bid, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_bid = serializer.save()
        return Response({
            "Success": "Task bid modified successfully",
            "user": user.profile.username,
            "message": updated_bid.message
        }, status=status.HTTP_202_ACCEPTED)

    
    def delete(self, request, id, format=None):
        task = Task.objects.get(id=id)
        user = request.user
        account = Accounts_user.objects.get(email=user)
        try:
            bid = Bidder.objects.get(task=task, user=account)
        except Bidder.DoesNotExist:
            return Response({"Error": "Bid for task not found"}, status=status.HTTP_404_NOT_FOUND)
        
        bid.delete()
        return Response(
            {"Success": "Bid for task submitted successfully"},
        status=status.HTTP_204_NO_CONTENT)
    




class ApiTaskRequestView(APIView):
    permission_classes = (IsAuthenticated,)
    '''
    This view returns a list that shows all task that a
    user has requested for .....
    '''
    def get(self, request, format=None):
        user = request.user
        print(user)
        all_requested_tasks = Task.objects.filter(sender=user.id)
        serializer = TaskRequestSerializer(all_requested_tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ApiTaskErrandSerializer(APIView):
    permission_classes = (IsAuthenticated,)
    '''
    This view also returns a list of tasks where the authenticated user is the 
    messenger
    '''

    def get(self, request, format=None):
        user = request.user
        print(user.id)
        all_my__tasks = Task.objects.filter(messenger=user.id)
        serializer = TaskRequestSerializer(all_my__tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ApiMyTotalEarningView(APIView):
    permission_classes = (IsAuthenticated,)

    '''
    This view displays a users total earnings from
    all completed and paid errands
    '''

    def get(self, request, format=None):
        total_earnings = 0
        user = request.user
        all_my_tasks = Task.objects.filter(messenger=user.id)
        for task in all_my_tasks:
            if task.paid ==  True and task.completed == True:
                total_earnings += task.bidding_amount
        return Response({"total_earnings": total_earnings}, status=status.HTTP_200_OK)
    



class ApiNewBidderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        user = request.user
        task = Task.objects.get(id=id)
        new_bidder = NewBidder.objects.get(user=user, task=task)
        serializer = GetNewBidderSerializer(new_bidder)
        return Response(serializer.data)

    def post(self, request, id, format=None):
        user = request.user
        task = Task.objects.get(id=id)

        new_bidder = NewBidder.objects.create(user=user, task=task)
        serializer = PostBidderSerializer(new_bidder, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        




class ApiMyPerformanceView(APIView):
    '''
    Returns the users performance in percentage 
    '''
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        completed_tasks = 0 
        all_user_tasks = Task.objects.filter(messenger=user)
        total_no_of_tasks = len(all_user_tasks)
        for task in all_user_tasks:
            if task.completed == True:
                completed_tasks += 1
        performance_percentage = (completed_tasks/total_no_of_tasks) * 100
        return Response({"Your performance": f"{performance_percentage}%"}, status=status.HTTP_200_OK)




class ApiMyActivityView(APIView):
    def get(self, request, format=None):
        user = request.user
        completed_tasks = 0 
        all_user_tasks = Task.objects.filter(messenger=user)
        total_no_of_tasks = len(all_user_tasks)
        incomplete_tasks = 0
        if all_user_tasks.count() == 0:
            return Response({"Completion rate": "0%",
            "Incomplete": 0,
            "completed": 0}, status=status.HTTP_200_OK)

        for task in all_user_tasks:
            if task.completed == True:
                completed_tasks += 1
            else:
                incomplete_tasks += 1
        performance_percentage = (completed_tasks/total_no_of_tasks) * 100
        return Response({"Completion rate": f"{performance_percentage}%",
        "Incomplete": incomplete_tasks,
        "completed": completed_tasks}, status=status.HTTP_200_OK)
        
        


    # data = request.data
	# 	data['author'] = request.user.pk
	# 	serializer = BlogPostCreateSerializer(data=data)

	# 	data = {}


    # def post(self, request, format=None):
    #     serializer = self.serializer_class(data=request.data)


class ApiTaskAssignmentView(APIView):
    '''Retrieves all bidders for a particular task'''
    def get(self, request, *args, **kwargs):
        id = kwargs["id"]
        current_task = Task.objects.get(id=id)
        bidders = current_task.task_bidders.all()
        print(bidders)
        serializer = GetBidderSerializer(bidders, many=True)
        return Response({
        "Bidders": serializer.data
        }, status=status.HTTP_200_OK)
    


class ApiPostTaskAssignmentView(APIView):
    ''' Assigns the task to one of the task bidders
    Once a task is assigned to a user, the task field
    picked_up should change to True. The task also should stop 
    showing for others'''

    def post(self, request, *args, **kwargs):
        id = kwargs["id"]
        username = kwargs["username"]
        current_task = Task.objects.get(id=id)
        bidders = current_task.task_bidders.all()
        print(bidders)
        try:
            Bidder.objects.filter(task=Task.objects.get(id=id), user=CustomUser.objects.get(username=username).id)
        except Bidder.DoesNotExist:
            return Response("The user didn't bid for the task")
        except CustomUser.DoesNotExist:
            return Response({"Error": "The user doesn't exist"})
        

        if username == current_task.sender.username:
            return Response({"Error": "You caanot accept your own tasks"})

        current_task.messenger = CustomUser.objects.get(username=username)
        current_task.picked_up = True
        current_task.save()
        serializer = TaskSerializer(current_task)
        data = {"Success": f"You have successfully assigned the task to {username}",
                "Send a message": f"http://127.0.0.1:8000/chat/room/{id}/"}
        return Response(data, status=status.HTTP_202_ACCEPTED)
    

class ApiCurentTaskCompletedView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        current_user = request.user
        task_id = kwargs.get("id")
        current_task = get_object_or_404(Task, id=task_id)
        if current_task.sender == current_user:
            if current_task.picked_up ==True and current_task.being_delivered == True:
                current_task.completed = True
                commission_amount = Decimal(0.10) * Decimal(current_task.bidding_amount)
                our_commision = Commission.objects.create(task=current_task, amount=commission_amount)
                current_task.paid = True
                current_task.save()
                return Response({"Success": "Task has been completed and payment has been made"})
            return Response({"Error": "Task is still running"})
        return Response({"Message": "You don't have such rights"})
            
            

    


class ApiTaskSupport(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id, format=None):
        current_task = Task.objects.get(id=id)
        current_user = request.user
        
        support = Support(user=current_user, task=current_task)
        serializer = TaskSupportSerializer(support, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class ApiLabReportTaskView(APIView):
     
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  # Custom permission for GET requests
        elif self.request.method == 'POST':
            return [IsAuthenticated()]
        

    def get(self, request, format=None):
        lab_reports = LabReportTask.objects.all()
        serializer = LabReportSerializer(lab_reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        c_user = request.user
        user = Accounts_user.objects.get(email=c_user)
        new_lab_report = LabReportTask(sender=user)
        lab_report = LabReportSerializer(new_lab_report, data=request.data)
        lab_report.is_valid(raise_exception=True)
        lab_report.save()
        return Response({"Success": "Task creation successful"}, status=status.HTTP_201_CREATED)





class ApiUpdateLabReportTaskView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  # Custom permission for GET requests
        elif self.request.method == 'PUT':
            return [IsAuthenticated()]
        
    def get(self, request, slug, format=None):
        course = get_object_or_404(LabReportTask, task_slug=slug)
        serializer = LabReportSerializer(course)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    

    def put(self, request, slug, format=None):
        course = get_object_or_404(LabReportTask, task_slug=slug)
        if request.user != course.sender:
            raise serializers.ValidationError({"Response": "You do not have the permission to do this"})
        
        serializer = LabReportSerializer(course, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Success": "Task update successful"}, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request, slug, format=None):
        course = get_object_or_404(LabReportTask, task_slug=slug)
        course.delete()
        return Response({"Success": "Task deleted successfully"}, status=status.HTTP_200_OK)
    

class ApiLaundryTaskView(APIView):
    def post(self, request, format=None):
        c_user = request.user
        user = Accounts_user.objects.get(email=c_user)
        new_laundry = LaundryTask(sender=user)
        serializer = LaundryTaskSerializer(new_laundry, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Success": "Task created"})
    

class ApiDetailLaundryView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  # Custom permission for GET requests
        elif self.request.method == 'PUT':
            return [IsAuthenticated()]
        
    def get(self, request, slug, format=None):
        task = get_object_or_404(LaundryTask, task_slug=slug)
        serializer = LaundryTaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    

    def put(self, request, slug, format=None):
        task = get_object_or_404(LaundryTask, task_slug=slug)
        if request.user != task.sender:
            raise serializers.ValidationError({"Response": "You do not have the permission to do this"})
        
        serializer = LaundryTaskSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Success": "Task update successful"}, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request, slug, format=None):
        task = get_object_or_404(LaundryTask, task_slug=slug)
        task.delete()
        return Response({"Success": "Task deleted successfully"}, status=status.HTTP_200_OK)

    
    
    

        







    
