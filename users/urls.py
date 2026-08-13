from django.urls import path
from users.views import home, sign_up, Sign_in

urlpatterns = [
    path('home/', home, name='home'),
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', Sign_in.as_view(), name='sign-in'),
]
