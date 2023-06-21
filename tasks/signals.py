from django.db.models.signals import post_save
from .models import Shop, ShopProfile
from django.dispatch import receiver



@receiver(post_save, sender=Shop)
def create_shop_profile(sender, instance, created, **kwargs):
    if created:
        ShopProfile.objects.create(shop=instance)


@receiver(post_save, sender=Shop)
def save_shop_profile(sender, instance, **kwargs):
    instance.shopprofile.save()


