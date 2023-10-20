from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.conf import settings

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.signals import setting_changed
from django.dispatch import receiver
from django.utils.crypto import (
    RANDOM_STRING_CHARS,
    constant_time_compare,
    get_random_string,
    pbkdf2,
)
from django.utils.module_loading import import_string
from django.utils.translation import gettext_noop as _

UNUSABLE_PASSWORD_PREFIX = "!"  # This will never be a valid encoded hash
UNUSABLE_PASSWORD_SUFFIX_LENGTH = (
    40  # number of random chars to add after UNUSABLE_PASSWORD_PREFIX
)

class UserManager(BaseUserManager):
    def make_password(password, salt=None, hasher="default"):

        if password is None:
            return UNUSABLE_PASSWORD_PREFIX + get_random_string(
                UNUSABLE_PASSWORD_SUFFIX_LENGTH
            )
        if not isinstance(password, (bytes, str)):
            raise TypeError(
                "Password must be a string or bytes, got %s." % type(password).__qualname__
            )
        hasher = get_hasher(hasher)
        salt = salt or hasher.salt()
        return hasher.encode(password, salt)

    def set_password(self, raw_password):
        self.password = UserManager.make_password(raw_password)
        self._password = raw_password

    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        print(self.model)

        user = self.model(
            email=self.normalize_email(email)
            
        )

        # user = User(
        #     email=self.normalize_email(email),
        # )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_active = True
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

# hook in th
    
