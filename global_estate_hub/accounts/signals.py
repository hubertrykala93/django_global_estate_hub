from django.db.models.signals import post_save
from .models import User, Private, Company
from django.dispatch.dispatcher import receiver


@receiver(signal=post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Automatically creates a user profile upon successful registration.
    """
    if created:
        if instance.is_private:
            Private.objects.create(user=instance).save()


        elif instance.is_company:
            Company.objects.create(user=instance).save()
