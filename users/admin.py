from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Customer, Supplier


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """사용자 관리"""
    list_display = ['username', 'email', 'user_type', 'company_name', 'contact_phone', 'is_active', 'date_joined']
    list_filter = ['user_type', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'company_name', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('추가 정보', {
            'fields': ('user_type', 'company_name', 'contact_phone')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('추가 정보', {
            'fields': ('user_type', 'company_name', 'contact_phone')
        }),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """고객사 관리"""
    list_display = ['company_name', 'business_number', 'contact_person', 'contact_phone', 'contact_email', 'created_at']
    list_filter = ['created_at']
    search_fields = ['company_name', 'business_number', 'contact_person', 'contact_email']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'company_name', 'business_number')
        }),
        ('연락처 정보', {
            'fields': ('contact_person', 'contact_phone', 'contact_email', 'address')
        }),
        ('시스템 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """공급업체 관리"""
    list_display = ['company_name', 'business_number', 'contact_person', 'contact_phone', 'contact_email', 'created_at']
    list_filter = ['created_at']
    search_fields = ['company_name', 'business_number', 'contact_person', 'contact_email']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'company_name', 'business_number')
        }),
        ('연락처 정보', {
            'fields': ('contact_person', 'contact_phone', 'contact_email', 'address')
        }),
        ('시스템 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
