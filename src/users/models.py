import datetime
import random
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import random
import cloudinary.models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=255, unique=True)
    datecreated = models.DateTimeField(auto_now_add=True)
    occupation = models.CharField(max_length=100, null=True)
    profile_picture = cloudinary.models.CloudinaryField('', blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    languages = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.username:
            random_number = random.randint(100, 999)
            self.username = f"{self.first_name}{self.last_name}{random_number}"
        super().save(*args, **kwargs)

