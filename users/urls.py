from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CustomerViewSet, SupplierViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('customers', CustomerViewSet, basename='customer')
router.register('suppliers', SupplierViewSet, basename='supplier')

urlpatterns = [
    path('', include(router.urls)),
]
