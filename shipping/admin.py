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