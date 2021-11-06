from django.contrib import admin

from .models import Product, ProductImage, Category


admin.site.register(Category)


class ProductImageInline(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'short_description', 'category')
    search_fields = ('title', 'short_description', 'category')
    list_filter = ('category',)
    date_hierarchy = 'pub_datetime'
    inlines = [ProductImageInline]
