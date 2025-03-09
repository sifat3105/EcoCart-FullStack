from django.contrib import admin
from .models import ShoppigData

@admin.register(ShoppigData)
class ShoppigDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'division', 'district', 'upazila', 'address', 'number')
    list_filter = ('division', 'district', 'upazila')
    search_fields = ('user__username', 'district', 'upazila', 'number')
    raw_id_fields = ('user',)

    def __str__(self):
        return f"{self.user} - {self.district}"
    

from django.contrib import admin
from .models import ShippingUpdate

class ShippingUpdateAdmin(admin.ModelAdmin):
    # Display the fields in the admin list view
    list_display = ('order', 'status', 'timestamp', 'description')
    
    # Add search functionality by fields
    search_fields = ('order__id', 'status', 'description')
    
    # Add filtering options in the admin panel
    list_filter = ('status', 'timestamp')

    # Allow ordering by timestamp for ease of navigation
    ordering = ('-timestamp',)

    # Add a field for each row to be clickable, linking to the related order
    list_display_links = ('order',)

# Register the ShippingUpdate model with the custom admin interface
admin.site.register(ShippingUpdate, ShippingUpdateAdmin)
