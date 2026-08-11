from django.urls import path
from users.views import sign_up,Sign_in
urlpatterns = [
    path('sign-up/',sign_up,name='sign-up'),
    path('sign-in/',Sign_in.as_view(),name='sign-in'),
]
