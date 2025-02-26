from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=255, unique=True)
    phone_number = PhoneNumberField(region="BD", help_text="Enter a valid phone number.")
    business_license = models.CharField(max_length=255, unique=True)
    business_license_image = models.FileField(upload_to="business_license", max_length=100, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Seller"
        verbose_name_plural = "Sellers"
        ordering = ["shop_name"]

    def __str__(self):
        return self.shop_name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    phone_number = PhoneNumberField( region="BD", help_text="Enter a valid phone number.")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username