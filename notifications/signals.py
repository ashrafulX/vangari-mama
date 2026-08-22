from bids.models import Offer
from django.dispatch import receiver
from django.db.models.signals import post_save
from notifications.models import Notifications

@receiver(post_save,instance=Offer)
def  offer_created(sender,instance,created,**kwargs):
    if created:
        Notifications.objects.create(
            recipient=instance.listing.seller,
            message=f"New offer received for {instance.listing.title}",
            link=f"/bids/review-offer/"
        )