from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import Task
from rest_framework.response import Response

@receiver(post_save, sender=Task)
def initialize_paystack_payment(sender, created, instance, **kwargs):
    if created:
        return Response({"url": "https://api.paystack.co/transaction/initialize"})
