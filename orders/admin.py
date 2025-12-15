from django.contrib import admin
from .models import Order, OrderItem, ShippingInfo


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'size', 'price', 'subtotal']


class ShippingInfoInline(admin.StackedInline):
    model = ShippingInfo
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'user__username']
    list_editable = ['status']
    inlines = [OrderItemInline, ShippingInfoInline]
    readonly_fields = ['order_number', 'created_at', 'updated_at']


@admin.register(ShippingInfo)
class ShippingInfoAdmin(admin.ModelAdmin):
    list_display = ['order', 'full_name', 'phone', 'city', 'created_at']
    search_fields = ['full_name', 'phone', 'city', 'order__order_number']
    list_filter = ['city', 'created_at']
