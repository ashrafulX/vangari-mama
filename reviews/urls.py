from django.urls import path,include
from reviews.views import create_review
urlpatterns = [
    path('review/<int:id>/',create_review,name='review'),
    
    ]

