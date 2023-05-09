from rest_framework import serializers
from .models import Task, AcceptTask, TaskReview, Keyword, Bidder, NewBidder
from users.models import User

class KeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ["name"]


class PostNewBidderSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField("get_bidder_username")
    class Meta:
        model = NewBidder
        fields = ["message"]


class GetNewBidderSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewBidder
        fields = ["message"]

    # def get_bidder_username(self, obj):
    #     return obj.user.username


class GetBidderSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField("get_bidder_username")
    class Meta:
        model = Bidder
        fields = ["user", "message"]
    


class PostBidderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bidder
        fields = ["message"]

        
    

# class CreateTaskBidSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=100)
#     message = serializers.CharField(max_length=300)

 
#     def validate(self, attrs):
#         user = attrs.get("username")
#         if not User.objects.get(username=user):
#             raise ValueError({"Response": "No user found"})
#         return attrs
    

#     def create(self, validated_data):
#         username = validated_data["username"]
#         message = validated_data["message"]
#         user=User.objects.get(username=username)
#         if user:
#             comment=Bidder.objects.create(user=user, message=message)
#             payload={
#                 "username":comment.user__username,
#                 "message": message
#             }
#         return payload




class TaskSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField("get_name_of_sender")
    # url = serializers.HyperlinkedIdentityField(view_name='task-detail', lookup_field='id')
    # receiver_name = serializers.SerializerMethodField("get_name_of_receiver")
    # keywords = KeywordsSerializer()
    keywords = serializers.SerializerMethodField("get_actual_keyword")
    # task_bidders = serializers.SerializerMethodField("get_task_bidders")
    is_active = serializers.ReadOnlyField()
    completed = serializers.ReadOnlyField()
    paid = serializers.ReadOnlyField()
    class Meta:
        model = Task
        fields = ["id", "name", "description", "image", "bidding_amount", "sender", "sender_name", "keywords", "is_active",  "completed", "paid"]


    def get_name_of_sender(self, task_sender):
        username = task_sender.sender.username
        return username
    
    def get_actual_keyword(self, obj):
        return KeywordsSerializer(obj.keywords.all(), many=True).data
    
    # def get_task_bidders(self, obj):
    #     return GetBidderSerializer(obj.task_bidders.all(), many=True).data

    
    # def get_name_of_receiver(self, task_receiver):
    #     username = task_receiver.receiver.username
    #     return  username'''



class TaskDetailSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField("get_name_of_sender")
    # url = serializers.HyperlinkedIdentityField(view_name='task-detail', lookup_field='id')
    # receiver_name = serializers.SerializerMethodField("get_name_of_receiver")
    # keywords = KeywordsSerializer()
    keywords = serializers.SerializerMethodField("get_actual_keyword")
    # task_bidders = GetBidderSerializer()
    # task_bidders = serializers.SerializerMethodField("get_task_bidders")
    is_active = serializers.ReadOnlyField()
    completed = serializers.ReadOnlyField()
    paid = serializers.ReadOnlyField()
    class Meta:
        model = Task
        fields = ["id", "name", "description", "image", "bidding_amount", "sender", "sender_name", "keywords", "is_active", "task_bidders",  "completed", "paid"]


    def get_name_of_sender(self, task_sender):
        username = task_sender.sender.username
        return username
    
    def get_actual_keyword(self, obj):
        return KeywordsSerializer(obj.keywords.all(), many=True).data
    
    # def get_task_bidders(self, obj):
    #     return obj.task_bidders.all()
        # return GetBidderSerializer(obj.task_bidders.all(), many=True).data

    
    # def get_name_of_receiver(self, task_receiver):
    #     username = task_receiver.receiver.username
    #     return  username'''



class AcceptTaskSerializer(serializers.ModelSerializer):
    # receiver_name = serializers.SerializerMethodField("get_name_of_receiver")
    class Meta:
        model = AcceptTask

        fields = ["task", "receiver", "time_picked", "receiver_amount"]

    # def get_name_of_receiver(self, accepttask_receiver):
    #     username = accepttask_receiver.receiver.username
    #     return username


class TaskReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskReview

        fields = ['task', 'errander', 'errandee', 'comment', 'date_created']



class TaskRequestSerializer(serializers.ModelSerializer):
    '''
    This is to return a brief history of all tasks you have
    requested for on RUNAM...i.e you were the sender
    '''
    more_details = serializers.SerializerMethodField("generate_detail_link")
    bidding_amount = serializers.SerializerMethodField("add_naira_sign_to_bidding_amount")

    class Meta:
        model = Task
        fields = ["name", "more_details", "bidding_amount", "date_updated", "completed"]

    def generate_detail_link(self, obj):
        link = f"http://127.0.0.1:8000/tasks/{obj.id}"
        return link


    def add_naira_sign_to_bidding_amount(self, obj):
        sign =	u'\u20a6'
        new = f"{sign}{obj.bidding_amount}"
        return new
    


class MyTaskErrandSerializer(serializers.ModelSerializer):
    '''
    This is to return all tasks that a user has carried on
    i.e he was the messenger 
    '''
    class Meta:
        model = Task
        fields = ["name", "more_details", "bidding_amount", "date_updated", "completed"]

    def generate_detail_link(self, obj):
        link = f"http://127.0.0.1:8000/tasks/{obj.id}"
        return link


    def add_naira_sign_to_bidding_amount(self, obj):
        sign =	u'\u20a6'
        new = f"{sign}{obj.bidding_amount}"
        return new
    


class MyTotalEarningsSerializer(serializers.ModelSerializer):
    receiver_amount = serializers.SerializerMethodField("add_naira_sign_to_bidding_amount")
    class Meta:
        model = AcceptTask
        fields = ["receiver_amount"]

    def add_naira_sign_to_bidding_amount(self, obj):
        sign =	u'\u20a6'
        new = f"{sign}{obj.receiver_amount}"
        return new




    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


    


    

