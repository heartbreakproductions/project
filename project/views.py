from django.views.generic import TemplateView
from django.shortcuts import render
from notifications.models import Notification

# class Homepage(TemplateView):
#     template_name = 'index.html'
    
def get_unread_notification_count(user):
    """Helper function to get unread notification count for a user."""
    if user.is_authenticated:
        return Notification.objects.filter(recipient=user, read=False).count()
    return 0

class Homepage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unread_notification_count'] = get_unread_notification_count(self.request.user)
        return context


def donate_page(request):
    return render(request, 'donate_page.html')

    
def about_page(request):
    return render(request, 'about_page.html')