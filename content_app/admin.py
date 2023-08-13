from django.contrib import admin
from core.admin import custom_admin
from .models import Feedback

# register models to super admin with custom behaviour
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    list_filter = ['created_at']


# regoster models to custom admin with custom behaviour
custom_admin.register(Feedback, FeedbackAdmin)
