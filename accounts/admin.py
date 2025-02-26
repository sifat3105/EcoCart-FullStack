from django.contrib import admin
from .models import Seller, Customer

# Register the Seller model
@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'user', 'phone_number', 'is_active', 'is_verified')  # Fields to display in the list view
    list_filter = ('is_active', 'is_verified')  # Filters for the list view
    search_fields = ('shop_name', 'user__username', 'phone_number')  # Fields to search by
    readonly_fields = ('business_license_image',)  # Make certain fields read-only

    # Customize the form for adding/editing a Seller
    fieldsets = (
        (None, {
            'fields': ('user', 'shop_name', 'phone_number')
        }),
        ('Business Details', {
            'fields': ('business_license', 'business_license_image', 'address')
        }),
        ('Status', {
            'fields': ('is_active', 'is_verified')
        }),
    )

# Register the Customer model
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')  # Fields to display in the list view
    search_fields = ('user__username', 'phone_number')  # Fields to search by
    readonly_fields = ('profile_picture',)  # Make certain fields read-only

    # Customize the form for adding/editing a Customer
    fieldsets = (
        (None, {
            'fields': ('user', 'phone_number')
        }),
        ('Profile', {
            'fields': ('profile_picture',)
        }),
    )