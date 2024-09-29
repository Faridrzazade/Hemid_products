# products/admin.py

from django.contrib import admin
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('category', 'created_at')
    ordering = ('-created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating')
    search_fields = ('product__title', 'user__username')
    list_filter = ('rating',)
    ordering = ('-rating',)
