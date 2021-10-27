from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from urllib import request
from accounts.managers import UserManager

    
class Users(AbstractBaseUser, PermissionsMixin):
  
    TYPE = (
        ('seller', 'seller'),
        ('customer', 'customer'),
        ('admin', 'admin')
    )
    
    GENDER = (
        ('male', 'male'),
        ('female', 'female'),
        ('other', 'other')
    )

    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    middle_name = models.CharField(_('middle name'), max_length=150, null=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True, null=False)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    type = models.CharField(max_length=10, choices=TYPE, default=TYPE[0][0],null=False)
    phone = models.CharField(max_length=15, default=None, null=True)
    gender  = models.CharField(max_length=6, choices=GENDER, null=True)
    date_of_birth  = models.DateField(null=True)
    is_deleted=models.BooleanField(default=False)
    deleted_at=models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name


