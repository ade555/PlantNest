from django.urls import path
from .views import UserDeleteView, ProfileView, UpdateProfileView
app_name = "users"

urlpatterns = [
    path('', ProfileView.as_view(), name='view-profile'),
    path('update/', UpdateProfileView.as_view(), name='update-profile'),
    path('delete/', UserDeleteView.as_view(), name = "delete-profile"),
]
