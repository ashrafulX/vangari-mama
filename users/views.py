from django.shortcuts import render, redirect
from users.forms import RegisterModelForm, login_form ,CustomePasswordChangeForm,CustomPasswordResetForm,CustomPasswordConfirmResetForm,EditProfileModelForm
from django.contrib import messages
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordChangeDoneView ,PasswordResetView ,PasswordResetConfirmView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,UpdateView
from users.models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.urls import reverse_lazy
from listings.models import Listing,Category
from orders.models import Order
from bids.models import Offer
from allauth.socialaccount.models import SocialAccount
from django.core.paginator import Paginator
from django.db.models import Sum, Avg
from reviews.models import Review
# Create your views here.

def is_seller(request):
    return request.user.role=='SELLER'
def is_buyer(request):
    return request.user.role=='BUYER'

def is_admin(request):
    return request.user.groups.filter(name='Admin').exists()
""" 

"""

def dashboard(request):
#admin dashboard
    if request.user.groups.filter(name='Admin').exists():
        users = CustomUser.objects.all().order_by('-date_joined')
        listings = Listing.objects.select_related('seller', 'category').all().order_by('-created_at')
        categories = Category.objects.all().order_by('name')
        offers = Offer.objects.select_related('buyer', 'listing', 'listing__seller').all().order_by('-created_at')
        orders = Order.objects.select_related('buyer', 'seller', 'listing').all().order_by('-created_at')
        social_accounts = SocialAccount.objects.select_related('user').all()
        total_platform_sales = orders.aggregate(total=Sum('final_price'))['total'] or 0
        total_earnings = float(total_platform_sales) * 0.08

        admin_reviews = Review.objects.filter(reviewee=request.user)
        admin_rating = admin_reviews.aggregate(avg=Avg('rating'))['avg'] or 0.0
        admin_review_count = admin_reviews.count()

        context = {
            'users': users,
            'listings': listings,
            'categories': categories,
            'offers': offers,
            'orders': orders,
            'social_accounts': social_accounts,
            'total_earnings': round(total_earnings, 2),
            'admin_rating': round(admin_rating, 1),
            'admin_review_count': admin_review_count,
        }
        return render(request, 'dashboard/admin_dashboard.html', context)
    
    # 2. SELLER DASHBOARD
    elif is_seller(request):
        listing = Listing.objects.select_related('seller', 'category').filter(seller=request.user).order_by('-created_at')
        
        paginator = Paginator(listing, 5)
        page_number = request.GET.get('page')
        seller_listings = paginator.get_page(page_number)

        seller_orders = Order.objects.filter(seller=request.user)
        gross_sales = seller_orders.aggregate(total=Sum('final_price'))['total'] or 0
        net_income = float(gross_sales) * 0.92  # 92% goes to seller

        total_items_sold = seller_orders.count()
        active_listings_count = listing.filter(status='AVAILABLE').count()

        seller_reviews = Review.objects.filter(reviewee=request.user)
        seller_rating = seller_reviews.aggregate(avg=Avg('rating'))['avg'] or 0.0
        seller_review_count = seller_reviews.count()

        context = {
            'seller_listings': seller_listings,
            'gross_sales': round(gross_sales, 2),
            'net_income': round(net_income, 2),
            'total_items_sold': total_items_sold,
            'active_listings_count': active_listings_count,
            'seller_rating': round(seller_rating, 1),
            'seller_review_count': seller_review_count,
        }
        return render(request, 'dashboard/seller_dashboard.html', context)

    # 3. BUYER DASHBOARD
    elif is_buyer(request):
        buyer_orders = Order.objects.select_related('buyer', 'seller', 'listing').filter(buyer=request.user).order_by('-created_at')
        recent_purchases = buyer_orders[:5]

        total_bought_items = buyer_orders.count()
        total_spending = buyer_orders.aggregate(total=Sum('final_price'))['total'] or 0

        active_bids_count = Offer.objects.filter(buyer=request.user, status='PENDING').count()

        buyer_reviews = Review.objects.filter(reviewee=request.user)
        buyer_rating = buyer_reviews.aggregate(avg=Avg('rating'))['avg'] or 0.0
        buyer_review_count = buyer_reviews.count()

        context = {
            'recent_purchases': recent_purchases,
            'total_bought_items': total_bought_items,
            'total_spending': round(total_spending, 2),
            'active_bids_count': active_bids_count,
            'buyer_rating': round(buyer_rating, 1),
            'buyer_review_count': buyer_review_count,
            'saved_items_count': 0, # If you have a wishlist model, count it here
        }
        return render(request, 'dashboard/buyer_dashboard.html', context)
    

    # 4. NO PERMISSION

    else:
        return render(request, 'error/no_permission.html')

# def dashboard(request):

#     if request.user.groups.filter(name='Admin').exists():

#         users = CustomUser.objects.all().order_by('-date_joined')
#         listings = Listing.objects.select_related('seller', 'category').all().order_by('-created_at')
#         categories = Category.objects.all().order_by('name')
#         offers = Offer.objects.select_related( 'buyer', 'listing', 'listing__seller').all().order_by('-created_at')
#         orders = Order.objects.select_related('buyer', 'seller', 'listing').all().order_by('-created_at')
#         social_accounts = SocialAccount.objects.select_related( 'user').all()
#         context = {
#             'users': users,
#             'listings': listings,
#             'categories': categories,
#             'offers': offers,
#             'orders': orders,
#             'social_accounts': social_accounts,
#         }

#         return render( request, 'dashboard/admin_dashboard.html',context)
    
#     # elif is_seller(request):
#     #     listing=Listing.objects.select_related('seller','category').filter(seller=request.user).order_by('-created_at')
       
#     #     paginator = Paginator(listing, 8)

#     #     page_number = request.GET.get('page')
#     #     seller_listings = paginator.get_page(page_number)
#     #     context={
#     #                 'seller_listings':listing,
#     #             }
#     #     return render(request,'dashboard/seller_dashboard.html',context)

#     elif is_seller(request):
#         listing = Listing.objects.select_related(
#             'seller', 'category'
#         ).filter(
#             seller=request.user
#         ).order_by('-created_at')

#         paginator = Paginator(listing, 5)

#         page_number = request.GET.get('page')
#         seller_listings = paginator.get_page(page_number)

#         context = {
#             'seller_listings': seller_listings,
#         }

#         return render( request,'dashboard/seller_dashboard.html',context)
    
#     elif is_buyer(request):
#         recent_purchases=Order.objects.select_related('buyer','seller','listing').filter(buyer=request.user).order_by('-created_at')[:5]

#         context={
#             'recent_purchases':recent_purchases,
            
#         }
#         return render(request,'dashboard/buyer_dashboard.html',context)
    
#     else:
#         return render(request,'error/no_permission.html')


def sign_up(request):
    form = RegisterModelForm()

    if request.method == 'POST':
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(request, "Account Create successfully. Check your E-mail to Activate your Account!")
            return redirect('sign-in')

    return render(request, 'registration/sign_up.html', {'form': form})


class Sign_in(LoginView):
    template_name = 'registration/sign_in.html'
    form_class = login_form

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()



def activate_user(requtest,id,token):
    try:
        user=CustomUser.objects.get(id=id)
        if default_token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid user or Token')
    except user.DoesNotExist:
        return HttpResponse('User not Found')

class ProfileView(LoginRequiredMixin,TemplateView):
    template_name='account/profile.html'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        user=self.request.user
        context['username']=user.username
        context['email']=user.email
        context['name']=user.get_full_name()
        context['member_since']=user.date_joined
        context['last_login']=user.last_login
        context['address']=user.address
        context['district']=user.district
        context['role']=user.role

        return context



class ChangePassword(LoginRequiredMixin,PasswordChangeView):
    template_name='account/password_change.html'
    form_class=CustomePasswordChangeForm


class CustomPasswordResetView(PasswordResetView):
    form_class=CustomPasswordResetForm
    template_name='registration/send_email.html'
    success_url=reverse_lazy('sign-in')
    html_email_template_name='registration/reset_email.html'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['protocol']='https' if self.request.is_secure() else 'http'
        context['domain']=self.request.get_host()
        return context

    def form_valid(self,form):
        messages.success(self.request,'A Reset Email send! Please Check Your Email')
        return super().form_valid(form)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class=CustomPasswordConfirmResetForm
    template_name='registration/reset_password.html'
    success_url=reverse_lazy('sign-in')


    def form_valid(self,form):
        messages.success(self.request,'Password Reset Succesfully!')
        return super().form_valid(form)


class EditProfileView(LoginRequiredMixin,UpdateView):
    model=CustomUser
    form_class=EditProfileModelForm
    context_object_name='form'
    template_name='account/edit_profile.html'

    def get_object(self,):
        return self.request.user

    def form_valid(self,form):
        form.save()
        return redirect('profile')


