from django.contrib import admin
from .models import Plant, PlantCategory, Products, CartItem, Cart

from core.admin import custom_admin

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ['product', 'quantity', 'get_product_type']
    readonly_fields = ['product', 'quantity', 'get_product_type']
    def has_add_permission(self, request, obj):
        return False
    
    def get_product_type(self, obj):
        return obj.product.product_type
    get_product_type.short_description = 'Product Type'

class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ['user', 'created_at', 'get_total_price', 'get_product_type']
    list_filter = ['created_at', 'user__username', 'cartitem__product__product_type']
    search_fields = ['user__username', 'cartitem__product__product_name']
    readonly_fields = ['user']

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'

    def get_product_type(self, obj):
        return obj.cartitem_set.first().product.product_type
    get_product_type.short_description = 'Product Type'

    # def changelist_view(self, request, extra_context=None):
    #     if hasattr(self, 'search_term') and self.search_term:
    #         extra_context = extra_context or {}
    #         extra_context['placeholder'] = 'Search products'
    #     return super().changelist_view(request, extra_context=extra_context)



# Register your models here.
custom_admin.register(Plant)
custom_admin.register(Products)
custom_admin.register(PlantCategory)
custom_admin.register(CartItem)
custom_admin.register(Cart, CartAdmin)