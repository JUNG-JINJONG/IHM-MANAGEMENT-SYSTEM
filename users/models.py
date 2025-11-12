from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """커스텀 사용자 모델"""
    
    USER_TYPE_CHOICES = [
        ('operator', '운영자'),
        ('supplier', '공급업체'),
        ('customer', '고객사'),
    ]
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, verbose_name='사용자 유형')
    company_name = models.CharField(max_length=200, blank=True, verbose_name='회사명')
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name='연락처')
    
    class Meta:
        db_table = 'users'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class Customer(models.Model):
    """고객사 (선주사)"""
    
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='customer_profile', verbose_name='사용자 계정')
    company_name = models.CharField(max_length=200, verbose_name='회사명')
    business_number = models.CharField(max_length=50, unique=True, verbose_name='사업자번호')
    address = models.TextField(blank=True, verbose_name='주소')
    contact_person = models.CharField(max_length=100, verbose_name='담당자')
    contact_phone = models.CharField(max_length=20, verbose_name='연락처')
    contact_email = models.EmailField(verbose_name='이메일')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    class Meta:
        db_table = 'customers'
        verbose_name = '고객사'
        verbose_name_plural = '고객사'
    
    def __str__(self):
        return self.company_name


class Supplier(models.Model):
    """공급업체"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='supplier_profile', verbose_name='사용자 계정')
    company_name = models.CharField(max_length=200, verbose_name='회사명')
    business_number = models.CharField(max_length=50, unique=True, verbose_name='사업자번호')
    address = models.TextField(blank=True, verbose_name='주소')
    contact_person = models.CharField(max_length=100, verbose_name='담당자')
    contact_phone = models.CharField(max_length=20, verbose_name='연락처')
    contact_email = models.EmailField(verbose_name='이메일')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    class Meta:
        db_table = 'suppliers'
        verbose_name = '공급업체'
        verbose_name_plural = '공급업체'
    
    def __str__(self):
        return self.company_name
