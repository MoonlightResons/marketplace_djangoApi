from django.contrib import admin
from .models import Product, Basket, BasketItem, Category


class BasketItemInline(admin.TabularInline):
    model = BasketItem
    extra = 0


class CartAdmin(admin.ModelAdmin):
    inlines = [BasketItemInline]
    list_display = ('customer', 'created_at')


admin.site.register(Basket, CartAdmin)
admin.site.register(Product)
admin.site.register(Category)