from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User,Profile
@receiver(post_save,sender=User)
def save_profile(sender,instance,created,**extra):
    
    if created:
      
        user=Profile.objects.create(user=instance)
        user.save()