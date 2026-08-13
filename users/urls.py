from django.urls import path
from users.views import  sign_up, Sign_in , activate_user ,ProfileView , ChangePassword ,CustomPasswordResetView,CustomPasswordResetConfirmView,EditProfileView
from django.contrib.auth.views import LogoutView , PasswordChangeDoneView


urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', Sign_in.as_view(), name='sign-in'),
    path('activate/<int:id>/<str:token>/',activate_user),
    path('sign-out/',LogoutView.as_view(),name='logout'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('change-password/',ChangePassword.as_view(),name='change-password'),
    path('change-password/done/',PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'),name='password_change_done'),
    path('reset-password/',CustomPasswordResetView.as_view(),name='password_reset'),
    path('reset-password/confirm/<uidb64>/<token>/',CustomPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('edit-profile/',EditProfileView.as_view(),name='edit-profile'),

]
