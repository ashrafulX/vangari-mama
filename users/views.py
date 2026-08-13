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


  

# Create your views here.




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