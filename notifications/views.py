from django.shortcuts import render,redirect
from notifications.models import Notifications
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

# Create your views here.

class NotificationsView(LoginRequiredMixin,ListView):
    model=Notifications
    context_object_name = 'allnotification'
    template_name='notifications.html'
    paginate_by = 5

    def get_queryset(self):
        queryset=Notifications.objects.filter(recipient=self.request.user).order_by('-created_at')
        return queryset


def openNotificatins(request,id):
    specific=Notifications.objects.get(id=id,recipient=request.user)

    specific.is_read=True
    specific.save(update_fields=['is_read'])
    return redirect(f'/{specific.link}')
