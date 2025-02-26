from django.db import models

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    payment_method = models.CharField(max_length=50)
    shipping_address = models.TextField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)