from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import User

@receiver(pre_save, sender=User)
def ensure_required_fields(sender, instance, **kwargs):
    # Check if any of the required fields are empty
    if not instance.first_name or not instance.last_name or not instance.email:
        raise ValueError("Required user fields (first_name, last_name, email) must be provided.")
