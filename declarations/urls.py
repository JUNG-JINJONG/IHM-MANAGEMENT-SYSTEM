from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PurchaseOrderViewSet, DeclarationRequestViewSet,
    DeclarationViewSet, HazardousMaterialViewSet
)

router = DefaultRouter()
router.register('purchase-orders', PurchaseOrderViewSet, basename='purchaseorder')
router.register('declaration-requests', DeclarationRequestViewSet, basename='declarationrequest')
router.register('declarations', DeclarationViewSet, basename='declaration')
router.register('hazardous-materials', HazardousMaterialViewSet, basename='hazardousmaterial')

urlpatterns = [
    path('', include(router.urls)),
]
