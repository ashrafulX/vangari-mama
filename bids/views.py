from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.views.generic import DetailView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from users.views import is_buyer
from listings.models import Listing
from django.contrib.auth.decorators import login_required
from bids.models import Offer
from users.views import is_seller,is_buyer
from django.contrib import messages 
# Create your views here.

@login_required
def make_offer(request,id):

    if not is_buyer(request):
        return render(request,'error/no_permission.html')
    
    listing=get_object_or_404(Listing,id=id)
    if request.method=='POST':
        amount=request.POST.get('amount')

        Offer.objects.create(
            listing=listing,
            buyer=request.user,
            offer_price=amount,
            status='PENDING'
        )
        return redirect('view-details',id=id)
    return redirect('view-details',id=id)

class Review_offer(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model=Offer
    context_object_name='offers'
    template_name='bid/seller_offers.html'

    def test_func(self):
        return is_seller(self.request)

    def get_queryset(self):
        return Offer.objects.filter(listing__seller=self.request.user,status='PENDING').select_related('listing','buyer')


@login_required
def accept_offer(request,id):

    if not is_seller(request):
        return render(request,'error/no_permission.html')

    offer=get_object_or_404(Offer,id=id)
    if offer.listing.seller != request.user:
        return render(request,'error/no_permission.html')

    offer.status='ACCEPTED'
    offer.save(update_fields=['status'])
    messages.success(request,'Offer has been Accepted!')
    return redirect('review-offer') #dashboard


@login_required
def reject_offer(request,id):
    if not is_seller(request):
        return render(request,'error/no_permission.html')
    
    offer=get_object_or_404(Offer,id=id)
    if offer.listing.seller != request.user:
        return render(request,'error/no_permission.html')
    
    offer.status='REJECTED'
    offer.save(update_fields=['status'])
    messages.success(request,'Offer Has been Rejected!')
    return redirect('review-offer') #dashboard


@login_required
def biddingview(request):

    if not is_buyer(request):
        return render(request,'error/no_permission.html')

    bids=Offer.objects.filter(buyer=request.user).order_by('-created_at')

    return render(request,'bid/bidding_list.html',{'bids':bids})


@login_required
def offers(request):
    if not is_seller(request):
        return render(request,'error/no_permission.html')

    bids=Offer.objects.filter(listing__seller=request.user).order_by('-created_at')
    return render(request,'bid/offer_list.html',{'bids':bids})
