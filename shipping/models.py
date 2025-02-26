from django.db import models
from django.contrib.auth.models import User

class ShoppigData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="shippig")
    division = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    upazila = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField()
    number = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.district}"