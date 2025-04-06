from django.contrib import admin
from apps.products.models.categories import Category
from apps.products.models.products import Product
from apps.products.models.characteristics import Characteristic, CharacteristicOption


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'parent_category')  # Исправил 'main_category' на 'parent_category'
    search_fields = ('title',)
    filter_horizontal = ('characteristics',)
    list_filter = ('parent_category',)  # Исправил 'main_category' на 'parent_category'
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
    list_display = ('id', 'title')  # Убрал 'category', так как поля с таким именем нет
    search_fields = ('title',)
    list_filter = ()  # Убрал 'category', так как у характеристики нет связи с категорией
    ordering = ('title',)


# Регистрация моделей в админке
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Characteristic, CharacteristicAdmin)
admin.site.register(CharacteristicOption, CharacteristicOptionAdmin)
