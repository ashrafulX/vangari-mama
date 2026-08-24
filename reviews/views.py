from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from orders.models import Order
from .models import Review
from .forms import ReviewModelForm
# Create your views here.

@login_required
def create_review(request, id):

    order = get_object_or_404(Order.objects.select_related('buyer', 'seller'),id=id)

    if request.user != order.buyer and request.user != order.seller:
        return render(request, 'error/no_permission.html')

    if request.user == order.buyer:
        reviewer = order.buyer
        reviewee = order.seller
    else:
        reviewer = order.seller
        reviewee = order.buyer

    if Review.objects.filter(order=order,reviewer=reviewer,reviewee=reviewee).exists():
        messages.error(request,'You have already reviewed this order.')
        return redirect('order-details', id=id)

    if request.method == 'POST':

        form = ReviewModelForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.order = order
            review.reviewer = reviewer
            review.reviewee = reviewee
            review.save()
            messages.success(request,'Review submitted successfully!')
            return redirect('order-details', id=id)

    else:
        form = ReviewModelForm()

    return render(request,'create_review.html',{'form': form,'order': order,'reviewee': reviewee,})