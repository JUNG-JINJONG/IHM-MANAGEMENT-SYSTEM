from django.contrib import admin
from .models import Ship


@admin.register(Ship)
class ShipAdmin(admin.ModelAdmin):
    """선박 관리"""
    list_display = ['ship_name', 'imo_number', 'customer', 'ship_type', 'gross_tonnage', 'year_built', 'is_active', 'created_at']
    list_filter = ['is_active', 'ship_type', 'year_built', 'created_at']
    search_fields = ['ship_name', 'imo_number', 'customer__company_name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('customer', 'ship_name', 'imo_number')
        }),
        ('선박 상세', {
            'fields': ('ship_type', 'gross_tonnage', 'year_built', 'is_active')
        }),
        ('시스템 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
