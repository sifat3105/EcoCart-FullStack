from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from order.models import Order

class ShoppigData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="shippig")
    full_name = models.CharField(max_length=100, blank=True, null=True)
    division = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    upazila = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField()
    number = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.district}"
    



class ShippingUpdate(models.Model):
    order = models.ForeignKey(Order, related_name='shipping_updates', on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=[
        ('Processing', 'Processing'),             # Order being processed
        ('Shipped', 'Shipped'),                   # Order shipped
        ('Picked up', 'Picked up'),               # Order picked up by the courier
        ('In Transit', 'In Transit'),             # Order is on the way
        ('Out for Delivery', 'Out for Delivery'), # Order out for delivery
        ('Delivered', 'Delivered'),               # Order delivered to customer
        ('Delayed', 'Delayed'),                   # Shipping delayed
        ('Returned', 'Returned'),                 # Order returned
        ('Cancelled', 'Cancelled'),               # Order cancelled
    ])
    timestamp = models.DateTimeField(default=timezone.now)
    description = models.TextField(null=True, blank=True)  # Description for the status update

    def __str__(self):
        return f"Shipping update for Order {self.order.id}: {self.status} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']  # Ensure updates are ordered by the most recent first
