from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        print("user","user")
        user.save()
        return user


    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)


        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('superuser must have is_superuser=True'))
        return self.create_user(email, password, **extra_fields)


user_type_choice = (
        (1,'Admin'),
        (2,'BDE')
    )


class CustomUser(AbstractUser):
    username = None
    name = models.CharField(null=True, blank=True, max_length=128)
    email = models.EmailField(null=True, blank=True, max_length=128, unique=True)
    password = models.CharField(null=True, blank=True, max_length=128)
    clickup_id = models.BigIntegerField(null=True, blank=True)
    user_type = models.IntegerField(choices=user_type_choice, default=2)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email