from django.contrib.auth.models import AbstractUser
from django.db import models
from .utils import validate_image_size

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profile_picture = models.ImageField(
        upload_to='profile_pictures',
        default='default.png',
        blank=True,
        null=True,
        validators=[validate_image_size]
    )

    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'phone_number']

    def __str__(self):
        return self.username