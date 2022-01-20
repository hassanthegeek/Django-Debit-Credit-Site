from django.db.models.signals import post_save
from .models import CustomUser
from accounts.models import Account
from django.dispatch import receiver


@receiver(post_save, sender=CustomUser)
def create_account(sender, instance, created, **kwargs):
    print(kwargs)
    print(sender)
    print(instance)
    if created:
        Account.objects.create(user=instance)
