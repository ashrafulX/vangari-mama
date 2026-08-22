from django.urls import path,include
from bids.views import make_offer,Review_offer,accept_offer,reject_offer,biddingview,offers
urlpatterns = [
    path('make-offer/<int:id>/',make_offer,name='make-offer'),
    path('review-offer/',Review_offer.as_view(),name='review-offer'),
    path('accept-offer/<int:id>/',accept_offer,name='accept-offer'),
    path('reject-offer/<int:id>/',reject_offer,name='reject-offer'),
    path('my-bids/',biddingview,name='my-bids'),
    path('my-offers/',offers,name='offers'),
]