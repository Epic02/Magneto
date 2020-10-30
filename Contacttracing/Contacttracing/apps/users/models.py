from datetime import datetime

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, User
from django.contrib.postgres.fields import JSONField
from django.contrib.auth import get_user_model

from mew.core.models import BaseModel
from simple_history.models import HistoricalRecords

from .manager import CustomUserManager


class AppEnums(BaseModel):
    """
    """
    category = models.CharField(max_length=254)
    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254)
    weight = models.FloatField()
    is_active = models.BooleanField(default=True)


class User(AbstractBaseUser, BaseModel):
    """
    """
    first_name = models.CharField(max_length=254)
    middle_name = models.CharField(max_length=254, blank=True, default="")
    last_name = models.CharField(max_length=254, blank=True)
    # , doctor, admin, superadmin
    username = models.CharField(max_length=254, unique=True)
    email = models.EmailField(max_length=254, default="", unique=False)
    phone = models.CharField(max_length=50, default="", unique=False)
    aadhar_number = models.CharField(max_length=12, default="", unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    profile_pic = models.CharField(max_length=254)
    date_of_birth = models.DateTimeField(default=datetime.strptime("31/12/9999 23:59:59", "%d/%m/%Y %H:%M:%S"))
    gender = models.CharField(max_length=50)

    currency = models.CharField(max_length=254)
    language = models.CharField(max_length=254)
    timezone = models.CharField(max_length=254)

    history = HistoricalRecords()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()

    class Meta:
        db_table = 'api_user'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return self.first_name
