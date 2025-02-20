from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    user_type_choices = (
        ('customer', 'Customer'),
        ('restaurant', 'Restaurant'),
        ('driver', 'Driver'),
    )
    user_type = models.CharField(max_length=20, choices=user_type_choices, default='customer')

    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)
