from django.db import models
from users.models import Customer


class Ship(models.Model):
    """선박"""
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='ships', verbose_name='고객사')
    ship_name = models.CharField(max_length=200, verbose_name='선박명')
    imo_number = models.CharField(max_length=20, unique=True, verbose_name='IMO 번호')
    ship_type = models.CharField(max_length=100, blank=True, verbose_name='선박 종류')
    gross_tonnage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='총톤수')
    year_built = models.IntegerField(null=True, blank=True, verbose_name='건조년도')
    is_active = models.BooleanField(default=True, verbose_name='활성 상태')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    class Meta:
        db_table = 'ships'
        verbose_name = '선박'
        verbose_name_plural = '선박'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.ship_name} ({self.imo_number})"
