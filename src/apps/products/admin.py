from django.contrib import admin

from apps.products.models import Cart, CartProduct
from apps.products.models.categories import Category
from apps.products.models.products import Product
from apps.products.models.characteristics import Characteristic, CharacteristicOption


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'parent_category')
    search_fields = ('title',)
    filter_horizontal = ('characteristics',)
    list_filter = ('parent_category',)
    ordering = ('title',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'amount', 'seller_id', 'category', 'description')
    search_fields = ('title', 'description')
    list_filter = ('category', 'product_characteristics')
    filter_horizontal = ('product_characteristics',)
    ordering = ('title',)


class CharacteristicOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'characteristic')
    search_fields = ('title',)
    list_filter = ('characteristic',)
    ordering = ('title',)


class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)
    list_filter = ()
    ordering = ('title',)


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'created_at')
    search_fields = ('user_id',)
    readonly_fields = ('created_at',)
    list_filter = ('created_at',)


class CartProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product_id', 'quantity')
    search_fields = ('product_id', 'cart__user_id')
    readonly_fields = ()
    list_filter = ()



admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Characteristic, CharacteristicAdmin)
admin.site.register(CharacteristicOption, CharacteristicOptionAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartProduct, CartProductAdmin)
