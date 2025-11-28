from django.contrib import admin
from .models import Shirt, Color, Font


@admin.register(Shirt)
class ShirtAdmin(admin.ModelAdmin):
    list_display = ['color', 'existence', 'image']
    list_filter = ['color', 'existence']
    search_fields = ['color', 'existence']


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['color']


@admin.register(Font)
class FontAdmin(admin.ModelAdmin):
    list_display = ['name', 'font']
    list_filter = ['name']
    search_fields = ['name']
