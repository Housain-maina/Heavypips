from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_signalmanager', False)
        extra_fields.setdefault('is_newslettermanager', False)
        extra_fields.setdefault('allowaccess', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_signalmanager', True)
        extra_fields.setdefault('is_newslettermanager', True)
        extra_fields.setdefault('allowaccess', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_signalmanager') is not True:
            raise ValueError('Superuser must have is_signalmanager=True.')
        if extra_fields.get('is_newslettermanager') is not True:
            raise ValueError('Superuser must have is_newslettermanager=True.')
        if extra_fields.get('allowaccess') is not True:
            raise ValueError('Superuser must have allowaccess=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True,
                              error_messages={
                                  'unique': _("A user with that email already exists."),
                              },
                              max_length=150,
                              )
    phone = PhoneNumberField(max_length=30, unique=True, null=True, blank=False,
                             error_messages={
                                 'unique': _("A user with that phone number already exists."),
                             },
                             help_text='We will be sending you signals through this phone number.'
                             )


    allowaccess = models.BooleanField(_('allow access'), default=False, null=True, blank=True, help_text='allow access to signals')
    is_signalmanager = models.BooleanField(_('is signal manager'), default=False,
                                           help_text='let this user post signals', null=True, blank=True)
    is_newslettermanager = models.BooleanField(_('is newsletter manager'),default=False,
                                               help_text='let this user send newsletters', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
