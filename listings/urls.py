from django.urls import path,include
from listings.views import CreateCategoryView,ListingCreateView,Edit_listing,EditListingView,MarketPlaceView
urlpatterns = [
    path('create-category/',CreateCategoryView.as_view(),name='create-category'),
    path('listing/',ListingCreateView.as_view(),name='listing'),
    path('edit-listing/<int:id>/',EditListingView.as_view(),name='edit-listing'),
    path('marketplace/',MarketPlaceView.as_view(),name='marketplace')

]