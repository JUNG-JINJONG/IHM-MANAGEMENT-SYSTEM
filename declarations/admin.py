from django.contrib import admin
from .models import PurchaseOrder, DeclarationRequest, Declaration, HazardousMaterial


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    """구매 주문 관리"""
    list_display = ['order_number', 'ship', 'title', 'item_name', 'quantity', 'unit', 'order_date', 'delivery_date', 'status', 'created_at']
    list_filter = ['status', 'order_date', 'delivery_date', 'created_at']
    search_fields = ['order_number', 'title', 'item_name', 'ship__ship_name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    date_hierarchy = 'order_date'
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('order_number', 'ship', 'title', 'description', 'created_by')
        }),
        ('품목 정보', {
            'fields': ('item_name', 'item_description', 'quantity', 'unit')
        }),
        ('일정 및 상태', {
            'fields': ('order_date', 'delivery_date', 'status')
        }),
        ('시스템 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DeclarationRequest)
class DeclarationRequestAdmin(admin.ModelAdmin):
    """신고서 요청 관리"""
    list_display = ['id', 'purchase_order', 'supplier', 'request_date', 'due_date', 'status', 'created_at']
    list_filter = ['status', 'request_date', 'due_date', 'created_at']
    search_fields = ['purchase_order__order_number', 'supplier__company_name']
    readonly_fields = ['request_date', 'created_at', 'updated_at']
    ordering = ['-created_at']
    date_hierarchy = 'request_date'
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('purchase_order', 'supplier', 'created_by')
        }),
        ('일정 및 상태', {
            'fields': ('request_date', 'due_date', 'status')
        }),
        ('시스템 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class HazardousMaterialInline(admin.TabularInline):
    """신고서 내 유해물질 인라인 표시"""
    model = HazardousMaterial
    extra = 1
    fields = ['material_name', 'cas_number', 'content_percentage', 'location_in_product']


@admin.register(Declaration)
class DeclarationAdmin(admin.ModelAdmin):
    """신고서 관리"""
    list_display = ['id', 'declaration_type', 'item_name', 'supplier', 'ship', 'compliance_status', 'status', 'submitted_date', 'approved_date']
    list_filter = ['declaration_type', 'compliance_status', 'status', 'submitted_date', 'approved_date', 'created_at']
    search_fields = ['item_name', 'manufacturer', 'model_number', 'supplier__company_name', 'ship__ship_name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    date_hierarchy = 'submitted_date'
    inlines = [HazardousMaterialInline]
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('declaration_request', 'supplier', 'ship', 'declaration_type')
        }),
        ('품목 정보', {
            'fields': ('item_name', 'manufacturer', 'model_number')
        }),
        ('적합성 정보', {
            'fields': ('compliance_status', 'certification_number', 'hazardous_materials_json')
        }),
        ('전자서명', {
            'fields': ('supplier_signature', 'supplier_name', 'signature_date')
        }),
        ('제출 및 승인', {
            'fields': ('status', 'submitted_date', 'approved_by', 'approved_date', 'rejection_reason')
        }),
        ('시스템 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(HazardousMaterial)
class HazardousMaterialAdmin(admin.ModelAdmin):
    """유해물질 관리"""
    list_display = ['material_name', 'cas_number', 'content_percentage', 'declaration', 'location_in_product', 'created_at']
    list_filter = ['material_name', 'created_at']
    search_fields = ['material_name', 'cas_number', 'declaration__item_name']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('물질 정보', {
            'fields': ('declaration', 'material_name', 'cas_number', 'content_percentage')
        }),
        ('상세 정보', {
            'fields': ('location_in_product', 'remarks')
        }),
        ('시스템 정보', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
