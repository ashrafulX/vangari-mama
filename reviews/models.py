from django.db import models
from users.models import CustomUser
from orders.models import Order
# Create your models here.

class Review(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE,related_name='reviews')
    reviewer=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='given')
    reviewee=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='received')
    rating=models.PositiveSmallIntegerField()
    comment=models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'reviewer', 'reviewee'],
                name='unique_review_per_order'
            )
        ]

    def __str__(self):
        return f'{self.reviewer} → {self.reviewee} ({self.rating})'

