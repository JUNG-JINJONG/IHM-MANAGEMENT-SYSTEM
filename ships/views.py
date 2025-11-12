from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Ship
from .serializers import ShipSerializer, ShipListSerializer


class ShipViewSet(viewsets.ModelViewSet):
    """선박 ViewSet"""
    queryset = Ship.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ShipListSerializer
        return ShipSerializer
    
    def get_queryset(self):
        queryset = Ship.objects.all()
        
        # 고객사 사용자는 자신의 선박만 조회
        if self.request.user.user_type == 'customer':
            queryset = queryset.filter(customer__user=self.request.user)
        
        # 쿼리 파라미터 필터링
        customer_id = self.request.query_params.get('customer', None)
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def my_ships(self, request):
        """내 회사 선박 목록"""
        if request.user.user_type != 'customer':
            return Response({'detail': '고객사 사용자만 접근 가능합니다.'}, status=403)
        
        ships = Ship.objects.filter(customer__user=request.user)
        serializer = self.get_serializer(ships, many=True)
        return Response(serializer.data)
