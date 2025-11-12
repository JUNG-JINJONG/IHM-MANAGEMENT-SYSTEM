from rest_framework import serializers
from .models import Ship
from users.serializers import CustomerSerializer


class ShipSerializer(serializers.ModelSerializer):
    """선박 Serializer"""
    customer_info = CustomerSerializer(source='customer', read_only=True)
    
    class Meta:
        model = Ship
        fields = ['id', 'customer', 'customer_info', 'ship_name', 'imo_number',
                  'ship_type', 'gross_tonnage', 'year_built', 'is_active',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ShipListSerializer(serializers.ModelSerializer):
    """선박 목록용 간단한 Serializer"""
    customer_name = serializers.CharField(source='customer.company_name', read_only=True)
    
    class Meta:
        model = Ship
        fields = ['id', 'ship_name', 'imo_number', 'customer_name', 'ship_type', 'is_active']
