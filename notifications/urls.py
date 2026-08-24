from django.urls import path
from notifications.views import NotificationsView,openNotificatins
urlpatterns = [
    path('notifications/',NotificationsView.as_view(),name='notifications'),
    path('read-notification/<int:id>/',openNotificatins,name='read-notification'),
]