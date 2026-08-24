from django.shortcuts import render,redirect
from orders.models import Order
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from users.views import is_admin,is_buyer,is_seller
from listings.models import Listing
from orders.models import Order
from decimal import Decimal
from django.contrib import messages
from django.views.generic import DetailView,ListView
from django.db.models import Q
from reviews.models import Review
# Create your views here.
class BuyListingView(LoginRequiredMixin,UserPassesTestMixin,View):
    
    def test_func(self):
        return is_buyer(self.request)
    def handle_no_permission(self):
        return render(self.request,'error/no_permission.html')
    
    # def get(self,request,id):
    #     listing=Listing.objects.get(id=id)
    #     if listing.status=='AVAILABLE':
    #         final_price=listing.price * listing.quantity
    #         commission_rate=Decimal('8')
    #         commission_amount=(final_price*commission_rate)/Decimal('100')

    #         order=Order.objects.create(
    #             listing=listing,
    #             buyer=request.user,
    #             seller=listing.seller,
    #             final_price=final_price,
    #             commission_rate=commission_rate,
    #             commission_amount=commission_amount,
    #         )

    #         listing.status='SOLD_OUT'
    #         listing.save(update_fields=['status'])
    #         messages.success(request,'Listing purchased successfully!')
    #     return redirect('order-details',id=order.id)

    def get(self, request, id):
        listing = Listing.objects.get(id=id)

        order = None

        if listing.status == 'AVAILABLE':
            final_price = listing.price * listing.quantity

            commission_rate = Decimal('8')
            commission_amount = (
                final_price * commission_rate
            ) / Decimal('100')

            order = Order.objects.create(
                listing=listing,
                buyer=request.user,
                seller=listing.seller,
                final_price=final_price,
                commission_rate=commission_rate,
                commission_amount=commission_amount,
            )

            listing.status = 'SOLD_OUT'
            listing.save(update_fields=['status'])

            messages.success(
                request,
                'Listing purchased successfully!'
            )

            return redirect('order-details', id=order.id)

        return redirect('view-details', id=listing.id)




class OrderDetailView(LoginRequiredMixin,UserPassesTestMixin,DetailView):
    model=Order
    pk_url_kwarg='id'
    template_name='order_details.html'       
        
    def get_queryset(self):
        queryset=Order.objects.select_related('buyer','seller','listing')
        return queryset             

    def get_object(self, queryset=None):
        if not hasattr(self, '_order_object'):
            self._order_object = super().get_object(queryset)

        return self._order_object                                                                                                                                                                    

    def test_func(self):
        user=self.request.user
        return (user == self.get_object().seller or user == self.get_object().buyer )
    
    def handle_no_permission(self):
        return render(self.request,'error/no_permission.html')


    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['item']=self.object.listing.title
        context['quantity']=self.object.listing.quantity
        context['image']=self.object.listing.image
        context['seller']=self.object.seller
        context['buyer']=self.object.buyer
        context['final_price']=self.object.final_price
        context['created_at']=self.object.created_at
        existing_review = Review.objects.filter(order=self.object,reviewer=self.request.user).exists()
        context['can_review'] =  not existing_review
        return context



class OrdersView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model=Order
    paginate_by = 10
    template_name='orders.html'
    context_object_name='orders'

    def test_func(self):
        return is_buyer(self.request) or is_seller(self.request)

    def get_queryset(self):
        queryset=Order.objects.select_related('buyer','seller','listing').filter(Q(buyer=self.request.user) | Q(seller=self.request.user))
        return queryset
