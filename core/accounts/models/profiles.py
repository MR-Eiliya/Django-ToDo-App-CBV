from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .users import CustomUserModel


# Profile class for better development
class Profile(models.Model):
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=CustomUserModel)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
