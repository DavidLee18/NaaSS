from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=254, blank=True)
    tel = models.CharField(validators=[RegexValidator(regex='^[0-9]{3}[-]+[0-9]{4}[-]+[0-9]{4}$')], max_length=254, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()