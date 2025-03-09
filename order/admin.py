from django.contrib import admin
from .models import Order, OrderItems, SellerOrder, SellerOrderItems

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer_name', 'email', 'customer_phone', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_id', 'customer_name', 'email')
    readonly_fields = ('created_at',)
    list_per_page = 20

@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('order__order_id', 'product__name')
    readonly_fields = ('created_at',)
    list_per_page = 20

@admin.register(SellerOrder)
class SellerOrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'seller', 'total', 'created_at')
    list_filter = ('created_at', 'seller')
    search_fields = ('order__order_id', 'seller__shop_name')
    readonly_fields = ('created_at',)
    list_per_page = 20

@admin.register(SellerOrderItems)
class SellerOrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('order__order__order_id', 'product__name')
    readonly_fields = ('created_at',)
    list_per_page = 20