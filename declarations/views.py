from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import PurchaseOrder, DeclarationRequest, Declaration, HazardousMaterial
from .serializers import (
    PurchaseOrderSerializer, PurchaseOrderListSerializer,
    DeclarationRequestSerializer, DeclarationSerializer,
    DeclarationListSerializer, DeclarationCreateSerializer,
    HazardousMaterialSerializer
)


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    """구매 주문 ViewSet"""
    queryset = PurchaseOrder.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PurchaseOrderListSerializer
        return PurchaseOrderSerializer
    
    def get_queryset(self):
        queryset = PurchaseOrder.objects.select_related('ship', 'created_by')
        
        # 고객사는 자신의 선박 PO만 조회
        if self.request.user.user_type == 'customer':
            queryset = queryset.filter(ship__customer__user=self.request.user)
        
        # 필터링
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        ship_id = self.request.query_params.get('ship', None)
        if ship_id:
            queryset = queryset.filter(ship_id=ship_id)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def request_declaration(self, request, pk=None):
        """신고서 요청 생성"""
        po = self.get_object()
        
        # 이미 요청이 있는지 확인
        if hasattr(po, 'declaration_request'):
            return Response({'detail': '이미 신고서 요청이 존재합니다.'},
                          status=status.HTTP_400_BAD_REQUEST)
        
        # supplier_id는 요청 데이터에서 받아야 함
        supplier_id = request.data.get('supplier')
        if not supplier_id:
            return Response({'detail': '공급업체를 선택해주세요.'},
                          status=status.HTTP_400_BAD_REQUEST)
        
        # 신고서 요청 생성
        declaration_request = DeclarationRequest.objects.create(
            purchase_order=po,
            supplier_id=supplier_id,
            due_date=request.data.get('due_date'),
            created_by=request.user
        )
        
        # PO 상태 업데이트
        po.status = 'requested'
        po.save()
        
        serializer = DeclarationRequestSerializer(declaration_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeclarationRequestViewSet(viewsets.ModelViewSet):
    """신고서 요청 ViewSet"""
    queryset = DeclarationRequest.objects.all()
    serializer_class = DeclarationRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = DeclarationRequest.objects.select_related(
            'purchase_order', 'supplier', 'created_by'
        )
        
        # 공급업체는 자신에게 온 요청만 조회
        if self.request.user.user_type == 'supplier':
            queryset = queryset.filter(supplier__user=self.request.user)
        
        # 고객사는 자신의 선박 관련 요청만 조회
        elif self.request.user.user_type == 'customer':
            queryset = queryset.filter(purchase_order__ship__customer__user=self.request.user)
        
        # 필터링
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """대기중인 신고서 요청 (공급업체용)"""
        if request.user.user_type != 'supplier':
            return Response({'detail': '공급업체 사용자만 접근 가능합니다.'}, status=403)
        
        requests_list = DeclarationRequest.objects.filter(
            supplier__user=request.user,
            status='pending'
        )
        serializer = self.get_serializer(requests_list, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """신고서 요청 승인 (운영자 전용)"""
        if request.user.user_type != 'operator':
            return Response({'detail': '운영자만 승인할 수 있습니다.'},
                          status=status.HTTP_403_FORBIDDEN)
        
        declaration_request = self.get_object()
        declaration_request.status = 'approved'
        declaration_request.save()
        
        serializer = self.get_serializer(declaration_request)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """신고서 요청 거절 (운영자 전용)"""
        if request.user.user_type != 'operator':
            return Response({'detail': '운영자만 거절할 수 있습니다.'},
                          status=status.HTTP_403_FORBIDDEN)
        
        declaration_request = self.get_object()
        declaration_request.status = 'rejected'
        declaration_request.rejection_reason = request.data.get('rejection_reason', '')
        declaration_request.save()
        
        serializer = self.get_serializer(declaration_request)
        return Response(serializer.data)


class DeclarationViewSet(viewsets.ModelViewSet):
    """신고서 ViewSet"""
    queryset = Declaration.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DeclarationListSerializer
        elif self.action == 'create':
            return DeclarationCreateSerializer
        return DeclarationSerializer
    
    def get_queryset(self):
        queryset = Declaration.objects.select_related(
            'declaration_request', 'supplier', 'ship', 'approved_by'
        ).prefetch_related('hazardous_materials')
        
        # 공급업체는 자신이 제출한 신고서만 조회
        if self.request.user.user_type == 'supplier':
            queryset = queryset.filter(supplier__user=self.request.user)
        
        # 고객사는 자신의 선박 신고서만 조회
        elif self.request.user.user_type == 'customer':
            queryset = queryset.filter(ship__customer__user=self.request.user)
        
        # 필터링
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        declaration_type = self.request.query_params.get('type', None)
        if declaration_type:
            queryset = queryset.filter(declaration_type=declaration_type)
        
        ship_id = self.request.query_params.get('ship', None)
        if ship_id:
            queryset = queryset.filter(ship_id=ship_id)
        
        return queryset
    
    def perform_create(self, serializer):
        declaration = serializer.save(
            submitted_date=timezone.now(),
            status='submitted'
        )
        # DeclarationRequest 상태 업데이트
        declaration.declaration_request.status = 'submitted'
        declaration.declaration_request.save()
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """신고서 승인 (운영자 전용)"""
        if request.user.user_type != 'operator':
            return Response({'detail': '운영자만 승인할 수 있습니다.'},
                          status=status.HTTP_403_FORBIDDEN)
        
        declaration = self.get_object()
        declaration.status = 'approved'
        declaration.approved_by = request.user
        declaration.approved_date = timezone.now()
        declaration.save()
        
        # DeclarationRequest 상태 업데이트
        declaration.declaration_request.status = 'approved'
        declaration.declaration_request.save()
        
        # PurchaseOrder 상태 업데이트
        po = declaration.declaration_request.purchase_order
        po.status = 'completed'
        po.save()
        
        serializer = self.get_serializer(declaration)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """신고서 거절 (운영자 전용)"""
        if request.user.user_type != 'operator':
            return Response({'detail': '운영자만 거절할 수 있습니다.'},
                          status=status.HTTP_403_FORBIDDEN)
        
        declaration = self.get_object()
        declaration.status = 'rejected'
        declaration.approved_by = request.user
        declaration.approved_date = timezone.now()
        declaration.rejection_reason = request.data.get('rejection_reason', '')
        declaration.save()
        
        # DeclarationRequest 상태 업데이트
        declaration.declaration_request.status = 'rejected'
        declaration.declaration_request.save()
        
        serializer = self.get_serializer(declaration)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_ship_declarations(self, request):
        """내 선박의 신고서 목록 (고객사용)"""
        if request.user.user_type != 'customer':
            return Response({'detail': '고객사 사용자만 접근 가능합니다.'}, status=403)
        
        declarations = Declaration.objects.filter(
            ship__customer__user=request.user,
            status='approved'
        )
        serializer = DeclarationListSerializer(declarations, many=True)
        return Response(serializer.data)


class HazardousMaterialViewSet(viewsets.ModelViewSet):
    """유해물질 ViewSet"""
    queryset = HazardousMaterial.objects.all()
    serializer_class = HazardousMaterialSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = HazardousMaterial.objects.select_related('declaration')
        
        # 신고서 ID로 필터링
        declaration_id = self.request.query_params.get('declaration', None)
        if declaration_id:
            queryset = queryset.filter(declaration_id=declaration_id)
        
        # 물질명으로 검색
        material_name = self.request.query_params.get('material_name', None)
        if material_name:
            queryset = queryset.filter(material_name__icontains=material_name)
        
        return queryset
