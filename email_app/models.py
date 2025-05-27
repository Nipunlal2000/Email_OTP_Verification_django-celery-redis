from django.db import models
from . manager import *
from django.contrib.auth.models import AbstractUser , Group , Permission
from django.utils import timezone

# Create your models here.


class UserProfile(AbstractUser):
 
    username = None
    email = models.EmailField(unique=True,null=True,blank=True)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    otp = models.IntegerField(null=True, blank=True)
   
    USERNAME_FIELD = 'email'
 
    REQUIRED_FIELDS = []
    groups = models.ManyToManyField(Group, related_name="profile_groups")  # ✅ Fix
    user_permissions = models.ManyToManyField(Permission, related_name="profile_permissions")
 
    objects = UserManager()
   
    def __str__(self):
        return self.email 