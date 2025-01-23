from django.contrib import admin
from .models import Category, Item

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    ordering = ('name',)

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}
    

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'slug', 'price', 'availability', 'created_at', 'updated_at')
    list_filter = ('availability', 'created_at', 'updated_at')
    ordering = ('name',)

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}