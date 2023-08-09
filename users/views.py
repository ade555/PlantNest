from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib.auth import get_user_model

from .forms import UserDeleteForm

User = get_user_model()
class UserDeleteView(LoginRequiredMixin, DeleteView):
    """
    Deletes the currently signed-in user and all associated data.
    """
    model = User
    template_name = 'user_deletion.html'
    success_url = reverse_lazy('account_signup')
    form_class = UserDeleteForm


    def delete(self, request, *args, **kwargs):

        # get the currently logged in user
        user = self.request.user

        # Logout before we delete. This will make the current user
        # unavailable (or actually, it points to AnonymousUser).
        logout(request)
        
        # Delete user (and any associated ForeignKeys, according to
        # on_delete parameters).
        user.delete()

        messages.success(request, 'Account successfully deleted')
        return super().delete(request, *args, **kwargs)