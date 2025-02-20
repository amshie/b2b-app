from django.contrib.auth import get_user_model
from django.db import models

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ausstehend'),
        ('preparing', 'In Zubereitung'),
        ('on_the_way', 'Unterwegs'),
        ('delivered', 'Geliefert'),
    ]
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    driver = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL, related_name="deliveries")

    def assign_driver(self):
        """Weist die Bestellung einem Fahrer zu."""
        available_drivers = get_user_model().objects.filter(user_type="driver")
        if available_drivers.exists():
            self.driver = available_drivers.order_by('?').first()  # Zufälliger Fahrer
            self.status = "on_the_way"
            self.save()
