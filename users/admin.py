from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import User
from core.admin import custom_admin

class CustomUserAdmin(UserAdmin):
    # List of fields to be shown in the user creation form
    add_fieldsets = (
        (None, {
            'fields': ('username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'profile_picture', 'is_active'),
        }),
    )

custom_admin.register(User, CustomUserAdmin)