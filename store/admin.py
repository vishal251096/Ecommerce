from django.contrib import admin
from .models import Product, Profile, ShippingAddress, Cart, OrderList

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'selling_price', 'description', 'category', 'brand', 'product_image']

@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'mobile', 'alternate_mobile']

admin.site.register(ShippingAddress)

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

@admin.register(OrderList)
class OrderListModelAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'address', 'status', 'date']