

import requests
from decouple import config
from django.contrib.auth import get_user_model     
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from PROJECT.settings import DEFAULT_FROM_EMAIL
from decouple import config

from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, Referral


from django.utils.crypto import get_random_string
from users.validators import validate_phone_number
from django.core.exceptions import ValidationError
from twilio.rest import Client

User = get_user_model()


@receiver(post_save, sender=User, dispatch_uid="unique_identifier")
def send_confirmation_email(sender, instance, created, **kwargs):
    if created:
        try:
            subject = 'Confirm Your Email Address'
            message = render_to_string('users/email_confirmation.html', {
            'user': instance,
            'domain': 'localhost:8000',
            'uid': urlsafe_base64_encode(smart_bytes(instance.pk)),
            'token': default_token_generator.make_token(instance),
        }) 
            from_email = DEFAULT_FROM_EMAIL
            to_email = instance.email
            # send_mail(subject, message, from_email, [to_email], fail_silently=False)
            msg = EmailMessage(subject, message, from_email, [to_email])
            msg.content_subtype = 'html'
            msg.send()
        except Exception as e:
            print(f'Error sending confirmation email: {e}')



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()



@receiver(post_save, sender=User)
def create_code(sender, instance, created, **kwargs):
    if created:
        Referral.objects.create(user=instance)



@receiver(post_save, sender=User)
def send_otp_sms(sender, instance, created, **kwargs):
    if created and instance.profile.is_complete:
        # Generate OTP
        otp = get_random_string(length=6, allowed_chars='0123456789')
        
        # Validate phone number
        try:
            validate_phone_number(instance.profile.phone_number)
        except ValidationError:
            return ValidationError
        
        # Send OTP via SMS
        account_sid = config('TWILIO_ACCOUNT_SID')
        auth_token = config('TWILIO_ACCOUNT_AUTH_TOKEN')
        twilio_number = config('TWILIO_PHONE_NUMBER')
        
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"Your OTP is: {otp}",
            from_=twilio_number,
            to="+2347052256260"
        )
        print(message.sid)
        
        # Save the OTP in the user's profile
        instance.profile.otp = otp
        instance.profile.save()
