from django.contrib import admin

from .models import Order, Receiver, Address


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('pk', 'status', 'user', 'total_price')
	raw_id_fields = ('address', 'receiver')
