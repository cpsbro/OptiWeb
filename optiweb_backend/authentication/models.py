from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, web_server_ip, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")
        if not web_server_ip:
            raise ValueError("The Web Server IP field must be set")
        user = self.model(email=email, username=username, web_server_ip=web_server_ip)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, web_server_ip, password=None):
        user = self.create_user(email, username, web_server_ip, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    web_server_ip = models.GenericIPAddressField(unique=True)  # Ensure IP is unique
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'web_server_ip']

    def __str__(self):
        return self.username
