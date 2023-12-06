from django.db.models.signals import post_save
from .models import User, Individual, Business
from django.dispatch.dispatcher import receiver


@receiver(signal=post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Automatically creates a individual or business profile upon successful registration.
    """
    if created:
        if instance.is_individual:
            Individual.objects.create(user=instance).save()


        elif instance.is_business:
            Business.objects.create(user=instance).save()
