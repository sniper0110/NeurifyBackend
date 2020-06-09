from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Customer

import os


def generate_customer_profile(sender, instance, created, **kwargs):

    if not instance.is_staff:
        if created:

            try:
                group = Group.objects.get(name='Freemium')
            except Group.DoesNotExist:
                print("\'FreemiumMember\' group does not exist!")
                pass
            else:
                instance.groups.add(group)
                username = instance.username
                email = instance.email

                Customer.objects.create(site_user=instance, username=username, email=email)

                print("A user has been created (of type Customer)")


post_save.connect(generate_customer_profile, sender=User)
