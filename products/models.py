from django.db import models
import uuid
from django.utils.text import slugify
from accounts.models import Seller
from django.core.files.base import ContentFile
from django.urls import reverse
import requests

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="products")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    short_description = models.TextField(null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)  # For file uploads
    image_url = models.URLField(max_length=1024, null=True, blank=True)  # For image URLs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, help_text="Weight in kilograms", null=True, blank=True)
    dimensions = models.CharField(max_length=50, help_text="Dimensions in cm (e.g., 110x33x100)", null=True, blank=True)
    materials = models.CharField(max_length=100, help_text="Material composition (e.g., 60% cotton)", null=True, blank=True)
    color = models.CharField(max_length=100, help_text="Available colors (e.g., Black, Blue, Grey)", null=True, blank=True)
    size = models.CharField(max_length=50, help_text="Available sizes (e.g., XL, L, M, S)", null=True, blank=True)
    sku = models.CharField(max_length=100, unique=True, help_text="Stock Keeping Unit", null=True, blank=True)
    brand = models.CharField(max_length=100, help_text="Product brand (e.g., Nike, Apple)", null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, help_text="Product rating (e.g., 4.5)", null=True, blank=True)
    discountPercentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Discount percentage (e.g., 15.00)", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + '-' + str(uuid.uuid4().hex[:6])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    # def save(self, *args, **kwargs):
    #     if self.image_url and not self.image:
    #         response = requests.get(self.image_url)
    #         if response.status_code == 200:
    #             self.image.save(
    #                 name=self.image_url.split('/')[-1],
    #                 content=ContentFile(response.content),
    #                 save=False
    #             )
    #     super().save(*args, **kwargs)

    def get_image(self):
        if self.image:
            return self.image.url
        elif self.image_url:
            return self.image_url
        else:
            return "path/to/default/image.jpg"
        


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    image_url = models.URLField(max_length=1024, null=True, blank=True) 
    is_default = models.BooleanField(default=False)  # Mark as default image

    def __str__(self):
        return f"Image for {self.product.name}"
    def save(self, *args, **kwargs):
        if self.image_url and not self.image:
            response = requests.get(self.image_url)
            if response.status_code == 200:
                self.image.save(
                    name=self.image_url.split('/')[-1],
                    content=ContentFile(response.content),
                    save=False
                )
        super().save(*args, **kwargs)