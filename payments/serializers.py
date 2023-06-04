from rest_framework import serializers
from tasks.models import Task, Keyword

class KeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ["name"]

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
        fields = ["id", "name", "description", "image", "bidding_amount", "sender_name", "keywords", "is_active",  "completed", "paid"]


    def get_name_of_sender(self, task_sender):
        username = task_sender.sender.username
        return username
    
    def get_actual_keyword(self, obj):
        return KeywordsSerializer(obj.keywords.all(), many=True).data