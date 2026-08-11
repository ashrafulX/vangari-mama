from django.shortcuts import render,redirect
from users.forms import RegisterModelForm,login_form
from django.contrib import messages
from django.contrib.auth.views import LoginView

# Create your views here.


def sign_up(request):

    form=RegisterModelForm()

    if request.method=='POST':
        form=RegisterModelForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            messages.success(request, "Account Createsuccesfully. Check your E-mail to Activate your Account!")
            return redirect('sign-in')

    return render(request,'registration/sign_up.html',{'form':form})

class Sign_in(LoginView):
    template_name = 'registration/sign_in.html'
    form_class=login_form
    def get_success_url(self):
        next_url=self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()