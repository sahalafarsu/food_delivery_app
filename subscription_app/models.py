from django.db import models

# Create your models here.
from django.contrib.auth.models import User


from django.db.models.signals import post_save
from django.dispatch import receiver

# Model to support Subscriptions


class CustomerStatus(models.Model):
    STATUSES = [
        ('active', 'active'),
        ('pause', 'pause'),
        ]

    status = models.CharField(max_length=15, choices=STATUSES, unique=True)

    def __str__(self):
        return self.status


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE,related_name="customer")
    stripeid = models.CharField(max_length=255,blank=True)
    stripe_subscription_id = models.CharField(max_length=255,blank=True)
    cancel_at_period_end = models.BooleanField(default=False)
    membership = models.BooleanField(default=False)

    status = models.ForeignKey(CustomerStatus, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return '{}'.format(self.user)


@receiver(post_save, sender=User)
def create_user_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_customer(sender, instance, **kwargs):
    instance.customer.save()


