from rest_framework import serializers
from .models import PurchaseOrder, DeclarationRequest, Declaration, HazardousMaterial
from ships.serializers import ShipListSerializer
from users.serializers import SupplierSerializer


class HazardousMaterialSerializer(serializers.ModelSerializer):
    """유해물질 Serializer"""
    
    class Meta:
        model = HazardousMaterial
        fields = ['id', 'declaration', 'material_name', 'cas_number', 
                  'content_percentage', 'location_in_product', 'remarks', 'created_at']
        read_only_fields = ['id', 'created_at', 'declaration']
        extra_kwargs = {
            'content_percentage': {'required': False},
            'material_name': {'required': False},
        }


class PurchaseOrderSerializer(serializers.ModelSerializer):
    """구매 주문 Serializer"""
    ship_info = ShipListSerializer(source='ship', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = PurchaseOrder
        fields = ['id', 'ship', 'ship_info', 'order_number', 'title', 'description',
                  'item_name', 'item_description', 'quantity', 'unit',
                  'order_date', 'delivery_date', 'status', 'created_by', 'created_by_username',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PurchaseOrderListSerializer(serializers.ModelSerializer):
    """구매 주문 목록용 Serializer"""
    ship_name = serializers.CharField(source='ship.ship_name', read_only=True)
    
    class Meta:
        model = PurchaseOrder
        fields = ['id', 'order_number', 'title', 'ship_name', 'item_name',
                  'quantity', 'unit', 'order_date', 'status']


class DeclarationRequestSerializer(serializers.ModelSerializer):
    """신고서 요청 Serializer"""
    order_number = serializers.CharField(source='purchase_order.order_number', read_only=True)
    supplier_name = serializers.CharField(source='supplier.company_name', read_only=True)
    ship_name = serializers.CharField(source='purchase_order.ship.ship_name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = DeclarationRequest
        fields = ['id', 'purchase_order', 'order_number', 'supplier', 'supplier_name',
                  'ship_name', 'request_date', 'due_date', 'status', 'created_by', 
                  'created_by_username', 'created_at', 'updated_at']
        read_only_fields = ['id', 'request_date', 'created_at', 'updated_at']


class DeclarationSerializer(serializers.ModelSerializer):
    """신고서 Serializer"""
    declaration_request_info = DeclarationRequestSerializer(source='declaration_request', read_only=True)
    supplier_info = SupplierSerializer(source='supplier', read_only=True)
    ship_info = ShipListSerializer(source='ship', read_only=True)
    hazardous_materials = HazardousMaterialSerializer(many=True, read_only=True)
    approved_by_username = serializers.CharField(source='approved_by.username', read_only=True)
    
    class Meta:
        model = Declaration
        fields = ['id', 'declaration_request', 'declaration_request_info', 'supplier', 'supplier_info',
                  'ship', 'ship_info', 'declaration_number', 'title', 'declaration_type', 'item_name', 
                  'manufacturer', 'model_number', 'hazardous_materials_json', 'compliance_status',
                  'certification_number', 'supplier_signature', 'supplier_name', 'signature_date',
                  'submitted_date', 'approved_date', 'approved_by', 'approved_by_username',
                  'status', 'rejection_reason', 'hazardous_materials', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class DeclarationListSerializer(serializers.ModelSerializer):
    """신고서 목록용 Serializer"""
    supplier_name = serializers.CharField(source='supplier.company_name', read_only=True)
    ship_name = serializers.CharField(source='ship.ship_name', read_only=True)
    purchase_order_title = serializers.CharField(source='declaration_request.purchase_order.title', read_only=True)
    
    class Meta:
        model = Declaration
        fields = ['id', 'declaration_number', 'title', 'purchase_order_title', 'declaration_type', 
                  'supplier_name', 'ship_name', 'compliance_status', 'status', 
                  'submitted_date', 'approved_date']


class DeclarationCreateSerializer(serializers.ModelSerializer):
    """신고서 생성용 Serializer (유해물질 포함)"""
    hazardous_materials = HazardousMaterialSerializer(many=True, required=False)
    
    # purchase_order를 받아서 declaration_request를 자동 생성/조회
    purchase_order = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Declaration
        fields = ['purchase_order', 'declaration_number', 'title',
                  'declaration_type', 'hazardous_materials']
        extra_kwargs = {
            'declaration_number': {'required': False},
            'title': {'required': False},
            'declaration_type': {'required': False},
        }
    
    def create(self, validated_data):
        from users.models import Supplier
        
        hazmat_data = validated_data.pop('hazardous_materials', [])
        purchase_order_id = validated_data.pop('purchase_order')
        
        # PurchaseOrder에서 정보 가져오기
        purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
        
        # 현재 사용자의 Supplier 가져오기
        supplier = Supplier.objects.get(user=self.context['request'].user)
        
        # DeclarationRequest 생성 또는 조회
        declaration_request, created = DeclarationRequest.objects.get_or_create(
            purchase_order=purchase_order,
            supplier=supplier,
            defaults={
                'created_by': self.context['request'].user,
                'status': 'pending'
            }
        )
        
        # Declaration 생성
        validated_data['declaration_request'] = declaration_request
        validated_data['supplier'] = supplier
        validated_data['ship'] = purchase_order.ship
        
        declaration = Declaration.objects.create(**validated_data)
        
        # 유해물질 생성
        for hazmat in hazmat_data:
            HazardousMaterial.objects.create(declaration=declaration, **hazmat)
        
        return declaration
