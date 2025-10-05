from django.contrib import admin
from .models import Product, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'quantity', 'price_cents')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at')  # Removed stripe_session_id & session_key
    inlines = [OrderItemInline]
    list_filter = ('status', 'created_at', 'user')
    search_fields = ('user__username',)

admin.site.register(Product)
