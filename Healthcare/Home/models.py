from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User
from Patient.models import Account
from django.conf import settings
from django.utils import timezone

class Become_member(models.Model):

    REQUIRED_FIELDS = ['Institution_name','Email_ID','Phone_Number','Source_of_Info']

    Institution_name = models.CharField(max_length=100)
    Email_ID = models.EmailField(verbose_name="email", max_length=60, unique=True)
    Phone_Number = models.CharField(max_length=10)
    Source_of_Info = models.CharField(max_length=100)

    def __str__(self):
        return self.Institution_name