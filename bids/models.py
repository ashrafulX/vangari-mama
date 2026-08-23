from django.db import models
from listings.models import Listing
from users.models import CustomUser
# Create your models here.
class Offer(models.Model):
    listing=models.ForeignKey(Listing,on_delete=models.CASCADE,related_name='offer')
    buyer=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='offer')
    offer_price=models.DecimalField(decimal_places=2,max_digits=10)
    status=models.CharField(max_length=20,choices=[('ACCEPTED','ACCEPTED'),('PENDING','PENDING'),('REJECTED','REJECTED')])
    created_at=models.DateTimeField(auto_now_add=True)

