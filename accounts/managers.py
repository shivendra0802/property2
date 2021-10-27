# from typing_extensions import runtime_checkable
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from urllib import request



class UserManager(BaseUserManager):
    # use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):

        if not email and request.data['type']  == 'customer':
            raise ValueError('The given email must be set')
        
        # elif not email and request.data['type']  == 'seller':
        #     raise ValueError('The given email must be set')

        # elif not email and request.data['type']  == 'admin':
        #     raise ValueError('The given email must be set')    
        # if not email:
        #     raise ValueError(_('The email have to enter'))    
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
        
    # def create_seller(self, email, password=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_active', True)

    #     if extra_fields.get('is_staff') is not True:
    #         raise ValueError('Seller must have is_staff=True.')

    #     return self._create_user(email, password, **extra_fields)  

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    