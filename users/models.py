from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.mail import send_mail
from .managers import UserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import os
import random
import string


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=254)
    first_name = models.CharField(verbose_name=_("First Name"), max_length=50)
    is_active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    date_joined = models.DateTimeField(auto_now_add=True)

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"] # Email & Password are required by default.

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(default="default2.jpg",upload_to="user_profile_pics", blank=True)
    bio = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=11)
    is_complete = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)


    def __str__(self):
        return f"{self.user.username} profile"

    @property
    def filename(self):
        return os.path.basename(self.image.name)
    



def generate_referral_code():
    # Generate a random referral code
    letters = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(letters) for _ in range(6))
    return code

class Referral(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True, default=generate_referral_code)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} code"
    





    