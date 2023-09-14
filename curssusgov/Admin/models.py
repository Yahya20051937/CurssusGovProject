from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission


# Create your models here.
class Admin(AbstractUser):
    adminName = models.CharField(max_length=20, unique=True)
    adminPassword = models.CharField(max_length=20, default='123')
    groups = models.ManyToManyField(Group, related_name='app_admins')
    username = models.CharField(unique=False, max_length=20)
    user_permissions = models.ManyToManyField(Permission, related_name='app_admins_permissions')
    role = 'admin$'
