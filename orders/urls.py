from django.urls import path,include
from orders.views import BuyListingView,OrderDetailView,OrdersView
urlpatterns = [
    path('buy-item/<int:id>',BuyListingView.as_view(),name='buy-item'),
    path('order-details/<int:id>',OrderDetailView.as_view(),name='order-details'),
    path('orders-view/',OrdersView.as_view(),name='orders-view')
]