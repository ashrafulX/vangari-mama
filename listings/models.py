from django.db import models
from users.models import CustomUser
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=50,null=False,unique=True)

    def __str__(self):
        return self.name
    
class Listing(models.Model):
    title=models.CharField(max_length=500,blank=False)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to='listings/',blank=True,null=True)
    status = models.CharField(max_length=20,choices=[("AVAILABLE", "Available"),("SOLD_OUT", "Sold Out"),],default="AVAILABLE")
    created_at=models.DateTimeField(auto_now_add=True)
    seller=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='listings')
    category=models.ForeignKey(Category,on_delete=models.PROTECT,related_name='listings')

    def __str__(self):
        return self.title