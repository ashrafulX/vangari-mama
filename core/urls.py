from django.urls import path,include
from core.views import base_view
urlpatterns = [
    path('base/',base_view,name='base-view'),
]