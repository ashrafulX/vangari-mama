from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("SELLER", "SELLER"),
        ("BUYER", "BUYER"),
    )
    profile_image=models.ImageField(upload_to='profile_images',blank=True)
    bio=models.TextField(blank=True)
    phone = PhoneNumberField(region='BD',blank=True)

    role=models.CharField(
            max_length=10,
            choices=ROLE_CHOICES,
            default='BUYER',
        )
    def __str__(self):
        return self.username
