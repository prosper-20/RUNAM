from django.db.models.signals import post_save
from .models import Shop, ShopProfile, Task
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail


@receiver(post_save, sender=Shop)
def create_shop_profile(sender, instance, created, **kwargs):
    if created:
        ShopProfile.objects.create(shop=instance)


@receiver(post_save, sender=Shop)
def save_shop_profile(sender, instance, **kwargs):
    instance.shopprofile.save()


@receiver(post_save, sender=Task)
def send_broadcast_mail(sender, instance, created, **kwargs):
    if created:
        subject = ' New Task Alert!!'
        message = f'A new task has been created, be the first to view it'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [instance.email]
        send_mail(subject, message, from_email, to_email, fail_silently=True)





# @receiver(post_save, sender=CustomUser)
# def send_activation_email(sender, instance, created, **kwargs):
#     if created:
#         subject = 'Welcome to our website'
#         message = f'Hi {instance.profile.username}, welcome to our website!'
#         from_email = settings.DEFAULT_FROM_EMAIL
#         to_email = [instance.email]
#         send_mail(subject, message, from_email, to_email, fail_silently=True)
        


