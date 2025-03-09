from django.contrib import admin
from .models import Payment, Refund

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payment_method', 'amount', 'status', 'transaction_id', 'created_at', 'updated_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('user__username', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment', 'amount', 'reason', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('payment__id', 'reason')
    readonly_fields = ('created_at',)
    list_per_page = 20