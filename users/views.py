from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from .models import User
from .forms import UserDeleteForm

# custom 404 error page view
def custom_404(request, exception):
    return render(request, '404.html', status=404)

class UserDeleteView(LoginRequiredMixin, DeleteView):
    """
    Deletes the currently signed-in user and all associated data.
    """
    model = User
    template_name = 'user_deletion.html'
    success_url = reverse_lazy('account_signup')
    form_class = UserDeleteForm

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()

        # Logout before we delete. This will make request.user
        # unavailable (or actually, it points to AnonymousUser).
        logout(request)
        
        # Delete user (and any associated ForeignKeys, according to
        # on_delete parameters).
        user.delete()
        messages.success(request, 'Account successfully deleted')
        return super().delete(request, *args, **kwargs)