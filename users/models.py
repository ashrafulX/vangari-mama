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

    address = models.TextField(
    blank=True,
    null=True
)

    district = models.CharField(
    max_length=50,
    choices=[
        ("Bagerhat", "Bagerhat"),
        ("Bandarban", "Bandarban"),
        ("Barguna", "Barguna"),
        ("Barishal", "Barishal"),
        ("Bhola", "Bhola"),
        ("Bogura", "Bogura"),
        ("Brahmanbaria", "Brahmanbaria"),
        ("Chandpur", "Chandpur"),
        ("Chattogram", "Chattogram"),
        ("Chuadanga", "Chuadanga"),
        ("Cox's Bazar", "Cox's Bazar"),
        ("Cumilla", "Cumilla"),
        ("Dhaka", "Dhaka"),
        ("Dinajpur", "Dinajpur"),
        ("Faridpur", "Faridpur"),
        ("Feni", "Feni"),
        ("Gaibandha", "Gaibandha"),
        ("Gazipur", "Gazipur"),
        ("Gopalganj", "Gopalganj"),
        ("Habiganj", "Habiganj"),
        ("Jamalpur", "Jamalpur"),
        ("Jashore", "Jashore"),
        ("Jhalokathi", "Jhalokathi"),
        ("Jhenaidah", "Jhenaidah"),
        ("Joypurhat", "Joypurhat"),
        ("Khagrachhari", "Khagrachhari"),
        ("Khulna", "Khulna"),
        ("Kishoreganj", "Kishoreganj"),
        ("Kurigram", "Kurigram"),
        ("Kushtia", "Kushtia"),
        ("Lakshmipur", "Lakshmipur"),
        ("Lalmonirhat", "Lalmonirhat"),
        ("Madaripur", "Madaripur"),
        ("Magura", "Magura"),
        ("Manikganj", "Manikganj"),
        ("Meherpur", "Meherpur"),
        ("Moulvibazar", "Moulvibazar"),
        ("Munshiganj", "Munshiganj"),
        ("Mymensingh", "Mymensingh"),
        ("Naogaon", "Naogaon"),
        ("Narail", "Narail"),
        ("Narayanganj", "Narayanganj"),
        ("Narsingdi", "Narsingdi"),
        ("Natore", "Natore"),
        ("Netrokona", "Netrokona"),
        ("Nilphamari", "Nilphamari"),
        ("Noakhali", "Noakhali"),
        ("Pabna", "Pabna"),
        ("Panchagarh", "Panchagarh"),
        ("Patuakhali", "Patuakhali"),
        ("Pirojpur", "Pirojpur"),
        ("Rajbari", "Rajbari"),
        ("Rajshahi", "Rajshahi"),
        ("Rangamati", "Rangamati"),
        ("Rangpur", "Rangpur"),
        ("Satkhira", "Satkhira"),
        ("Shariatpur", "Shariatpur"),
        ("Sherpur", "Sherpur"),
        ("Sirajganj", "Sirajganj"),
        ("Sunamganj", "Sunamganj"),
        ("Sylhet", "Sylhet"),
        ("Tangail", "Tangail"),
        ("Thakurgaon", "Thakurgaon"),
    ],
    blank=True,
    null=True
    )
    def __str__(self):
        return self.username
