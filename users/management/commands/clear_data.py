"""
Django management command to clear all dummy data from IHM Management System
Usage: python manage.py clear_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Customer, Supplier
from ships.models import Ship
from declarations.models import PurchaseOrder, DeclarationRequest, Declaration, HazardousMaterial

User = get_user_model()


class Command(BaseCommand):
    help = 'Clear all dummy data from IHM Management System (preserves superusers)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Starting data deletion...'))
        
        # Delete in correct order (respecting foreign key constraints)
        
        # 1. HazardousMaterial (no dependencies)
        hazmat_count = HazardousMaterial.objects.count()
        HazardousMaterial.objects.all().delete()
        self.stdout.write(f'Deleted {hazmat_count} hazardous materials')
        
        # 2. Declaration (has FK to HazardousMaterial)
        decl_count = Declaration.objects.count()
        Declaration.objects.all().delete()
        self.stdout.write(f'Deleted {decl_count} declarations')
        
        # 3. DeclarationRequest (has FK to Declaration)
        req_count = DeclarationRequest.objects.count()
        DeclarationRequest.objects.all().delete()
        self.stdout.write(f'Deleted {req_count} declaration requests')
        
        # 4. PurchaseOrder (has FK to DeclarationRequest)
        po_count = PurchaseOrder.objects.count()
        PurchaseOrder.objects.all().delete()
        self.stdout.write(f'Deleted {po_count} purchase orders')
        
        # 5. Ship (has FK to PurchaseOrder)
        ship_count = Ship.objects.count()
        Ship.objects.all().delete()
        self.stdout.write(f'Deleted {ship_count} ships')
        
        # 6. Supplier (has FK to Ship, PurchaseOrder, DeclarationRequest, Declaration)
        supplier_count = Supplier.objects.count()
        Supplier.objects.all().delete()
        self.stdout.write(f'Deleted {supplier_count} suppliers')
        
        # 7. Customer (has FK to Ship)
        customer_count = Customer.objects.count()
        Customer.objects.all().delete()
        self.stdout.write(f'Deleted {customer_count} customers')
        
        # 8. User (exclude superusers)
        user_count = User.objects.filter(is_superuser=False).count()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write(f'Deleted {user_count} users (preserved superusers)')
        
        self.stdout.write(self.style.SUCCESS('\nAll dummy data cleared successfully!'))
        self.stdout.write(self.style.SUCCESS('Superuser accounts have been preserved.'))
