from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Teacher


@receiver(post_save, sender=User)
def create_teacher_profile(sender, instance, created, **kwargs):
    """Automatically create Teacher profile when a new User is created (if needed)"""
    # This signal can be customized based on your needs
    # For now, it's just a placeholder for future enhancements
    pass


@receiver(post_save, sender=User)
def save_teacher_profile(sender, instance, **kwargs):
    """Save teacher profile when user is saved"""
    if hasattr(instance, 'teacher_profile'):
        instance.teacher_profile.save()