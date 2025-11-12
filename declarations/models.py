from django.db import models
from django.contrib.auth import get_user_model
from users.models import Supplier
from ships.models import Ship

User = get_user_model()


class PurchaseOrder(models.Model):
    """구매 주문"""
    
    STATUS_CHOICES = [
        ('pending', '대기'),
        ('requested', '요청됨'),
        ('completed', '완료'),
    ]
    
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, related_name='purchase_orders', verbose_name='선박')
    order_number = models.CharField(max_length=100, unique=True, verbose_name='주문번호')
    title = models.CharField(max_length=200, verbose_name='제목')
    description = models.TextField(blank=True, verbose_name='설명')
    item_name = models.CharField(max_length=200, blank=True, verbose_name='품목명')
    item_description = models.TextField(blank=True, verbose_name='품목 설명')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='수량')
    unit = models.CharField(max_length=50, blank=True, verbose_name='단위')
    order_date = models.DateField(verbose_name='주문일')
    delivery_date = models.DateField(null=True, blank=True, verbose_name='납품일')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='상태')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_purchase_orders', verbose_name='생성자')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    class Meta:
        db_table = 'purchase_orders'
        verbose_name = '구매 주문'
        verbose_name_plural = '구매 주문'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.order_number} - {self.title}"


class DeclarationRequest(models.Model):
    """신고서 요청"""
    
    STATUS_CHOICES = [
        ('pending', '대기'),
        ('submitted', '제출됨'),
        ('approved', '승인됨'),
        ('rejected', '거절됨'),
    ]
    
    purchase_order = models.OneToOneField(PurchaseOrder, on_delete=models.CASCADE, related_name='declaration_request', verbose_name='구매 주문')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='declaration_requests', verbose_name='공급업체')
    request_date = models.DateField(auto_now_add=True, verbose_name='요청일')
    due_date = models.DateField(null=True, blank=True, verbose_name='마감일')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='상태')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_declaration_requests', verbose_name='생성자')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    class Meta:
        db_table = 'declaration_requests'
        verbose_name = '신고서 요청'
        verbose_name_plural = '신고서 요청'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"요청 #{self.id} - {self.purchase_order.item_name}"


class Declaration(models.Model):
    """신고서 (MD/SDoC)"""
    
    DECLARATION_TYPE_CHOICES = [
        ('MD', 'Material Declaration'),
        ('SDoC', 'Supplier Declaration of Conformity'),
    ]
    
    COMPLIANCE_CHOICES = [
        ('compliant', '규정 준수'),
        ('non_compliant', '규정 미준수'),
    ]
    
    STATUS_CHOICES = [
        ('draft', '초안'),
        ('submitted', '제출됨'),
        ('approved', '승인됨'),
        ('rejected', '거절됨'),
    ]
    
    declaration_request = models.OneToOneField(DeclarationRequest, on_delete=models.CASCADE, related_name='declaration', verbose_name='신고서 요청')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='declarations', verbose_name='공급업체')
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, related_name='declarations', verbose_name='선박')
    
    declaration_number = models.CharField(max_length=50, unique=True, blank=True, verbose_name='신고서 번호')
    title = models.CharField(max_length=200, blank=True, verbose_name='제목')
    declaration_type = models.CharField(max_length=10, choices=DECLARATION_TYPE_CHOICES, blank=True, verbose_name='신고서 유형')
    item_name = models.CharField(max_length=200, blank=True, verbose_name='품목명')
    manufacturer = models.CharField(max_length=200, blank=True, verbose_name='제조사')
    model_number = models.CharField(max_length=100, blank=True, verbose_name='모델번호')
    
    hazardous_materials_json = models.JSONField(null=True, blank=True, verbose_name='유해물질 정보 (JSON)')
    compliance_status = models.CharField(max_length=20, choices=COMPLIANCE_CHOICES, blank=True, verbose_name='적합성 상태')
    certification_number = models.CharField(max_length=100, blank=True, verbose_name='인증번호')
    
    supplier_signature = models.CharField(max_length=200, blank=True, verbose_name='전자서명')
    supplier_name = models.CharField(max_length=100, blank=True, verbose_name='서명자명')
    signature_date = models.DateField(null=True, blank=True, verbose_name='서명일')
    
    submitted_date = models.DateTimeField(null=True, blank=True, verbose_name='제출일')
    approved_date = models.DateTimeField(null=True, blank=True, verbose_name='승인일')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_declarations', verbose_name='승인자')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='상태')
    rejection_reason = models.TextField(blank=True, verbose_name='거절 사유')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    class Meta:
        db_table = 'declarations'
        verbose_name = '신고서'
        verbose_name_plural = '신고서'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_declaration_type_display()} - {self.item_name}"


class HazardousMaterial(models.Model):
    """유해물질"""
    
    declaration = models.ForeignKey(Declaration, on_delete=models.CASCADE, related_name='hazardous_materials', verbose_name='신고서')
    material_name = models.CharField(max_length=200, blank=True, verbose_name='물질명')
    cas_number = models.CharField(max_length=50, blank=True, verbose_name='CAS 번호')
    content_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='함유율 (%)')
    location_in_product = models.CharField(max_length=200, blank=True, verbose_name='제품 내 위치')
    remarks = models.TextField(blank=True, verbose_name='비고')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    
    class Meta:
        db_table = 'hazardous_materials'
        verbose_name = '유해물질'
        verbose_name_plural = '유해물질'
    
    def __str__(self):
        return f"{self.material_name} ({self.content_percentage}%)"
