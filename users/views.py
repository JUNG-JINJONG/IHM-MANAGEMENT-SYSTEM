from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Customer, Supplier
from .serializers import (
    UserSerializer, CustomerSerializer, SupplierSerializer,
    UserRegistrationSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """사용자 ViewSet"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'register']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """회원가입"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'user_type': user.user_type,
                'message': '회원가입이 완료되었습니다.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """현재 로그인한 사용자 정보"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class CustomerViewSet(viewsets.ModelViewSet):
    """고객사 ViewSet"""
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Customer.objects.all()
        # 고객사 사용자는 자신의 정보만 조회
        if self.request.user.user_type == 'customer':
            queryset = queryset.filter(user=self.request.user)
        return queryset
    
    @action(detail=False, methods=['get'])
    def my_company(self, request):
        """내 고객사 정보"""
        try:
            customer = Customer.objects.get(user=request.user)
            serializer = self.get_serializer(customer)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response({'detail': '고객사 정보가 없습니다.'}, 
                          status=status.HTTP_404_NOT_FOUND)


class SupplierViewSet(viewsets.ModelViewSet):
    """공급업체 ViewSet"""
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Supplier.objects.all()
        # 공급업체 사용자는 자신의 정보만 조회
        if self.request.user.user_type == 'supplier':
            queryset = queryset.filter(user=self.request.user)
        return queryset
    
    @action(detail=False, methods=['get'])
    def my_company(self, request):
        """내 공급업체 정보"""
        try:
            supplier = Supplier.objects.get(user=request.user)
            serializer = self.get_serializer(supplier)
            return Response(serializer.data)
        except Supplier.DoesNotExist:
            return Response({'detail': '공급업체 정보가 없습니다.'}, 
                          status=status.HTTP_404_NOT_FOUND)
