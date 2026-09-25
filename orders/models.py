from django.db import models
from users.models import CustomUser
from listings.models import Listing
# Create your models here.
class Order(models.Model):
    listing=models.ForeignKey(Listing, on_delete=models.PROTECT,related_name='orders')
    buyer=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='orders')
    seller=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='sales')
    final_price=models.DecimalField(max_digits=10,decimal_places=2)
    commission_rate=models.DecimalField(max_digits=5,decimal_places=2,default=8.00)
    commission_amount=models.DecimalField(max_digits=5,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)