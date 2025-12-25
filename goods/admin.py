# goods/admin.py
from django.contrib import admin
from .models import Goods, GoodsImage, OutcomeImage, Message, Favorite

class GoodsImageInline(admin.TabularInline):
    """商品图片内联编辑"""
    model = GoodsImage
    extra = 1
    max_num = 3
    fields = ['image', 'order']


class OutcomeImageInline(admin.TabularInline):
    """Outcome图片内联编辑"""
    model = OutcomeImage
    extra = 1
    max_num = 5
    fields = ['image', 'order']


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'seller', 'major', 'category', 'created_at']
    list_filter = ['major', 'category', 'created_at', 'seller']
    search_fields = ['name', 'description', 'professor', 'course_code']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'price', 'description', 'seller')  # 添加seller
        }),
        ('Tags & Classification', {
            'fields': ('major', 'professor', 'category', 'course_code')
        }),
        ('Detailed Information', {
            'fields': ('amount_usage', 'payment_methods', 'additional_info'),
            'classes': ('collapse',)
        }),
        ('Outcome', {
            'fields': ('outcome_description',),
            'classes': ('collapse',)
        }),
    )

    inlines = [GoodsImageInline, OutcomeImageInline]


@admin.register(GoodsImage)
class GoodsImageAdmin(admin.ModelAdmin):
    list_display = ['goods', 'order', 'image']
    list_filter = ['goods']


@admin.register(OutcomeImage)
class OutcomeImageAdmin(admin.ModelAdmin):
    list_display = ['goods', 'order', 'image']
    list_filter = ['goods']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'item', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'created_at']
    list_filter = ['created_at']