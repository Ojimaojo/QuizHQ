from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Dashboard,Wallet

@receiver(post_save, sender=User)
def create_user_dashboard(sender, instance, created, **kwargs):
    if created:
        Dashboard.objects.create(user=instance)
        Wallet.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_dashboard(sender, instance, **kwargs):
    instance.dashboard.save()

@receiver(post_save, sender=User)
def save_user_wallet(sender, instance, **kwargs):
    instance.wallet.save()