from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Customer

def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name = 'customer')
        instance.groups.add(group)

        Customer.objects.create(
            user = instance,
            name = instance.username,
        )
    print('Profile created ......')
post_save.connect(customer_profile, sender = User)

# check apps.py ready method


# def update_profile (sender, instance, created, **kwargs):
#     if created == False:
#         instance.customer.save()
#         print('Customer updated ....')
# post_save.connect(update_profile, sender = User)
