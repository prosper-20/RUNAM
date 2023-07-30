from django.db.models.signals import post_save
from .models import Shop, ShopProfile, Task
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from users.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

@receiver(post_save, sender=Shop)
def create_shop_profile(sender, instance, created, **kwargs):
    if created:
        ShopProfile.objects.create(shop=instance)


@receiver(post_save, sender=Shop)
def save_shop_profile(sender, instance, **kwargs):
    instance.shopprofile.save()


# @receiver(post_save, sender=Task)
# def send_broadcast_mail(sender, instance, created, **kwargs):
#     if created:
#         subject = ' New Task Alert!!'
#         message = f'A new task has been created, be the first to view it'
#         from_email = settings.DEFAULT_FROM_EMAIL

#         # to_email = [user.email for user in User.objects.all()]
#         to_email = ["edwardprosper001@gmail.com", "edwardprosper002@gmail.com"]
#         send_mail(subject, message, from_email, to_email, fail_silently=True)


@receiver(post_save, sender=Task)
def send_broaadcast_mail(sender, instance, created, **kwargs):
    if created:
        subject = "New Task Alert !!"
        message = render_to_string('tasks/task_mail.html', {
            'domain': 'localhost:8000/users/login'
        })
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = ["edwardprosper001@gmail.com", "edwardprosper002@gmail.com"]
        # send_mail(subject, message, from_email, to_email)
        msg = EmailMessage(subject, message, from_email, to_email)
        msg.content_subtype = 'html'
        msg.send()


    
def send_email_on_accepted_change(sender, instance, **kwargs):
    if instance.completed:
        subject = 'Thank you for using RUNAM'
        message = 'Your task has been completed'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.messenger.email]
        send_mail(subject, message, from_email, recipient_list)





# @receiver(post_save, sender=CustomUser)
# def send_activation_email(sender, instance, created, **kwargs):
#     if created:
#         subject = 'Welcome to our website'
#         message = f'Hi {instance.profile.username}, welcome to our website!'
#         from_email = settings.DEFAULT_FROM_EMAIL
#         to_email = [instance.email]
#         send_mail(subject, message, from_email, to_email, fail_silently=True)
        


