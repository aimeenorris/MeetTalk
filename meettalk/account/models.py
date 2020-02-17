from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Account(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    email = models.EmailField()
    
    def __str__(self):
        return self.user
        
class Gymnast(models.Model):
    name = models.CharField('Gymnast Name', blank=False, max_length=60)
    # Add choices in the near future
    level = models.CharField('Gymnast Level', null=True, blank=True, default="", max_length=10)
    gym_name = models.CharField("Gym Name", null=True, blank=True, default="", max_length=60)
    birth_date = models.DateField(null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



@receiver(post_save, sender=User)
def create_user_account(sender, instance, created,**kwargs):
    if created:
        Account.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwarfs):
    instance.account.save()