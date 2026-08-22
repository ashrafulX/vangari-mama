from django.db import models
from users.models import CustomUser
# Create your models here.
class Notifications(models.Model):
    recipient=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='notifications')
    message=models.CharField(max_length=350)
    link=models.URLField(blank=True,null=True)
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)