from django.shortcuts import render,redirect
from listings.forms import CreateCategoryModelForm,ListingCreateModelForm
from django.views.generic import CreateView , UpdateView , DeleteView , ListView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from listings.models import Category,Listing
from django.contrib import messages
from django.urls import reverse_lazy
from users.views import is_seller,is_buyer,is_admin
# Create your views here.



class CreateCategoryView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model=Category
    template_name='create_category.html'
    fields=['name']
    success_url=reverse_lazy('create-category')

    def test_func(self):
        return is_admin(self.request)
    def handle_no_permission(self):
        return render(self.request,'error/no_permission.html')
    def form_valid(self,form):
        messages.success(self.request,'Category Created Succesfully!')
        return super().form_valid(form)

class ListingCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model=Listing
    template_name='create_listing.html'
    fields=['title','description','price','quantity','image','category']
    success_url=reverse_lazy('profile')

    def test_func(self):
        return is_seller(self.request)
    def form_valid(self, form):
        form.instance.seller=self.request.user
        return super().form_valid(form)
    
    def handle_no_permission(self):
        return render(self.request,'error/no_permission.html')

""" FunctionBaseView"""

def Edit_listing(request,id):
    listing=Listing.objects.get(id=id)
    form=ListingCreateModelForm(instance=listing)
    if request.method=='POST':
        form=ListingCreateModelForm(request.POST,request.FILES,instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request,'Edited Succesfulluy!')
            return redirect('profile') #after desing dashboard, return his dashboard
    return render(request,'edit_listing.html',{'form':form})


class EditListingView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    template_name='edit_listing.html'
    model=Listing
    pk_url_kwarg='id'
    context_object_name='form'
    form_class=ListingCreateModelForm
    success_url = reverse_lazy('profile')

    def test_func(self):
        return is_seller(self.request)
    
    def get_queryset(self):
        return Listing.objects.filter(seller=self.request.user)

    def handle_no_permission(self):
        return render(self.request,'error/no_permission.html')


    def form_valid(self, form):
        messages.success(self.request, 'Edited Successfully!')
        return super().form_valid(form)


#will implemented after implemnt role based Dashboard
class DeleteList(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Listing
    pk_url_kwarg = 'id'
    template_name='delete_listing_confirm.html'
    success_url=reverse_lazy('delete-listing-confirm')

    def test_func(self):
        return is_seller(self.request)
    
    def get_queryset(self):
        return Listing.objects.filter(seller=self.request.user)

    def handle_no_permission(self):
        return render(self.request,'error/no_permission.html')


class MarketPlaceView(ListView):
    model=Listing
    template_name='marketplace.html'
    context_object_name='lists'
    paginate_by = 10