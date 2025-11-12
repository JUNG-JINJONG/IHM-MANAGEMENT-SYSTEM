"""
Django management command to seed dummy data for IHM Management System
Usage: python manage.py seed_data
"""
import random
from datetime import datetime, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from users.models import Customer, Supplier
from ships.models import Ship
from declarations.models import PurchaseOrder, DeclarationRequest, Declaration, HazardousMaterial

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with dummy data for IHM Management System'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting data seeding...'))
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        HazardousMaterial.objects.all().delete()
        Declaration.objects.all().delete()
        DeclarationRequest.objects.all().delete()
        PurchaseOrder.objects.all().delete()
        Ship.objects.all().delete()
        Supplier.objects.all().delete()
        Customer.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        # Create users
        self.stdout.write('Creating users...')
        operators = self._create_operators(3)
        suppliers = self._create_suppliers(8)
        customers = self._create_customers(8)
        
        # Create ships
        self.stdout.write('Creating ships...')
        ships = self._create_ships(25, customers)
        
        # Create purchase orders and declarations
        self.stdout.write('Creating purchase orders and declarations...')
        purchase_orders = self._create_purchase_orders(70, ships, suppliers)
        
        # Create declaration requests
        self.stdout.write('Creating declaration requests...')
        declaration_requests = self._create_declaration_requests(purchase_orders)
        
        # Create declarations
        self.stdout.write('Creating declarations...')
        declarations = self._create_declarations(60, declaration_requests)
        
        # Create hazardous materials
        self.stdout.write('Creating hazardous materials...')
        self._create_hazardous_materials(180, declarations)
        
        self.stdout.write(self.style.SUCCESS('Data seeding completed successfully!'))
        self.stdout.write(f'Created: {len(operators)} operators, {len(suppliers)} suppliers, {len(customers)} customers')
        self.stdout.write(f'Created: {len(ships)} ships, {len(purchase_orders)} purchase orders')
        self.stdout.write(f'Created: {len(declaration_requests)} declaration requests, {len(declarations)} declarations')
        self.stdout.write(f'Created: ~180 hazardous materials')

    def _create_operators(self, count):
        """Create operator users"""
        operators = []
        for i in range(1, count + 1):
            user = User.objects.create_user(
                username=f'operator{i}' if i > 1 else 'operator',
                email=f'operator{i}@ihm-system.com',
                password='password123',
                user_type='operator',
                company_name='IHM Management Co.',
                contact_phone=f'02-{random.randint(1000,9999)}-{random.randint(1000,9999)}'
            )
            operators.append(user)
        return operators

    def _create_suppliers(self, count):
        """Create supplier users and supplier records"""
        companies = [
            'Marine Paint Korea', 'Ship Parts Supply', 'Naval Equipment Co.',
            'Ocean Tech Supplies', 'Maritime Solutions', 'SeaTech Industries',
            'Nautical Gear Ltd', 'Marine Components Korea'
        ]
        
        suppliers = []
        for i in range(count):
            user = User.objects.create_user(
                username=f'supplier{i+1}',
                email=f'supplier{i+1}@{companies[i].lower().replace(" ", "")}.com',
                password='password123',
                user_type='supplier',
                company_name=companies[i],
                contact_phone=f'02-{random.randint(1000,9999)}-{random.randint(1000,9999)}'
            )
            
            supplier = Supplier.objects.create(
                user=user,
                company_name=companies[i],
                business_number=f'{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(10000,99999)}',
                contact_person=f'{["Kim", "Lee", "Park"][i % 3]} Manager',
                contact_phone=user.contact_phone,
                contact_email=user.email,
                address=f'Seoul, Gangnam-gu, {random.randint(1,500)}-{random.randint(1,50)}'
            )
            suppliers.append(supplier)
        
        return suppliers

    def _create_customers(self, count):
        """Create customer users and customer records"""
        companies = [
            'Hanjin Shipping', 'Korea Marine Transport', 'Pacific Ocean Lines',
            'East Sea Shipping', 'Global Maritime Co.', 'Asian Cargo Lines',
            'Blue Ocean Shipping', 'Korea Vessel Management'
        ]
        
        customers = []
        for i in range(count):
            user = User.objects.create_user(
                username=f'customer{i+1}',
                email=f'customer{i+1}@{companies[i].lower().replace(" ", "")}.com',
                password='password123',
                user_type='customer',
                company_name=companies[i],
                contact_phone=f'051-{random.randint(1000,9999)}-{random.randint(1000,9999)}'
            )
            
            customer = Customer.objects.create(
                user=user,
                company_name=companies[i],
                business_number=f'{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(10000,99999)}',
                contact_person=f'{["Park", "Kim", "Lee"][i % 3]} Director',
                contact_phone=user.contact_phone,
                contact_email=user.email,
                address=f'Busan, Haeundae-gu, {random.randint(1,300)}-{random.randint(1,40)}'
            )
            customers.append(customer)
        
        return customers

    def _create_ships(self, count, customers):
        """Create ship records"""
        ship_types = ['Container Ship', 'Bulk Carrier', 'Tanker', 'Vehicle Carrier', 'General Cargo']
        ship_names = [
            'Pacific Dawn', 'Ocean Horizon', 'Sea Pioneer', 'Marine Star', 'Blue Wave',
            'Asia Express', 'Global Victory', 'Eastern Pride', 'Korean Spirit', 'Sea Fortune',
            'Ocean Glory', 'Pacific Dream', 'Marine Legend', 'Asia Pearl', 'Sea Champion',
            'Korea Express', 'Blue Ocean', 'East Wind', 'Pacific Queen', 'Ocean King',
            'Marine Prince', 'Asia Dragon', 'Sea Phoenix', 'Korea Pride', 'Global Voyager'
        ]
        
        ships = []
        for i in range(count):
            ship = Ship.objects.create(
                customer=random.choice(customers),
                ship_name=ship_names[i],
                imo_number=f'IMO{random.randint(1000000,9999999)}',
                ship_type=random.choice(ship_types),
                gross_tonnage=random.randint(5000, 100000),
                year_built=random.randint(2005, 2023),
                is_active=True
            )
            ships.append(ship)
        
        return ships

    def _create_purchase_orders(self, count, ships, suppliers):
        """Create purchase order records"""
        statuses = ['pending', 'requested', 'completed']
        weights = [0.3, 0.5, 0.2]  # Probability distribution
        
        items = [
            ('Marine Paint - Antifouling', 'High-quality antifouling paint for ship hull', 'liter'),
            ('Hydraulic Oil ISO 32', 'Marine grade hydraulic fluid', 'liter'),
            ('Engine Lubricant SAE 40', 'Heavy-duty marine engine oil', 'liter'),
            ('Electrical Cable 4mm', 'Marine-grade insulated copper cable', 'meter'),
            ('Steel Pipe Fittings', 'Stainless steel pipe connectors', 'piece'),
            ('Rubber Gaskets Set', 'EPDM rubber sealing gaskets', 'set'),
            ('Brake Pads', 'Industrial brake pad assemblies', 'set'),
            ('Cleaning Chemicals', 'Marine-safe degreaser and cleaner', 'liter'),
            ('Welding Electrodes E6013', 'General purpose welding rods', 'kg'),
        ]
        
        purchase_orders = []
        for i in range(count):
            order_date = datetime.now() - timedelta(days=random.randint(1, 180))
            delivery_date = order_date + timedelta(days=random.randint(7, 60))
            item = random.choice(items)
            
            po = PurchaseOrder.objects.create(
                ship=random.choice(ships),
                supplier=random.choice(suppliers),
                order_number=f'PO-{datetime.now().year}-{str(i+1).zfill(4)}',
                item_name=item[0],
                item_description=item[1],
                quantity=Decimal(str(random.randint(10, 500))),
                unit=item[2],
                order_date=order_date,
                delivery_date=delivery_date,
                status=random.choices(statuses, weights=weights)[0]
            )
            purchase_orders.append(po)
        
        return purchase_orders

    def _create_declaration_requests(self, purchase_orders):
        """Create declaration request records"""
        statuses = ['pending', 'submitted', 'approved', 'rejected']
        
        declaration_requests = []
        for po in purchase_orders:
            if po.status in ['requested', 'completed']:
                due_date = po.order_date + timedelta(days=random.randint(7, 14))
                
                dr = DeclarationRequest.objects.create(
                    purchase_order=po,
                    supplier=po.supplier,
                    due_date=due_date,
                    status='submitted' if po.status == 'completed' else 'pending'
                )
                declaration_requests.append(dr)
        
        return declaration_requests

    def _create_declarations(self, count, declaration_requests):
        """Create declaration records"""
        if not declaration_requests:
            return []
        
        declarations = []
        for dr in declaration_requests:
            if dr.status in ['submitted', 'approved']:
                declaration_type = random.choice(['MD', 'SDoC'])
                submitted_date_naive = dr.request_date + timedelta(days=random.randint(1, 7))
                # Convert to timezone-aware datetime
                submitted_date = timezone.make_aware(
                    datetime.combine(submitted_date_naive, datetime.min.time())
                )
                signature_date = submitted_date_naive
                
                approved_date = None
                if dr.status == 'approved':
                    approved_date_naive = submitted_date_naive + timedelta(days=random.randint(1, 5))
                    approved_date = timezone.make_aware(
                        datetime.combine(approved_date_naive, datetime.min.time())
                    )
                
                decl = Declaration.objects.create(
                    declaration_request=dr,
                    supplier=dr.supplier,
                    ship=dr.purchase_order.ship,
                    declaration_type=declaration_type,
                    item_name=dr.purchase_order.item_name,
                    manufacturer=random.choice([
                        'Korea Marine Industries', 'Global Ship Parts', 'Asia Marine Tech',
                        'Pacific Components', 'Marine Equipment Co.'
                    ]),
                    model_number=f'M-{random.randint(1000,9999)}-{random.randint(10,99)}',
                    compliance_status='compliant' if random.random() > 0.1 else 'non_compliant',
                    certification_number=f'CERT-{datetime.now().year}-{random.randint(1000,9999)}',
                    supplier_signature=f'SIGN_{dr.supplier.user.username}_{submitted_date_naive.strftime("%Y%m%d")}',
                    supplier_name=dr.supplier.contact_person,
                    signature_date=signature_date,
                    submitted_date=submitted_date,
                    status='approved' if dr.status == 'approved' else 'submitted',
                    approved_date=approved_date
                )
                declarations.append(decl)
        
        return declarations

    def _create_hazardous_materials(self, count, declarations):
        """Create hazardous material records"""
        if not declarations:
            return []
        
        materials = [
            {'name': 'Lead (Pb)', 'cas': '7439-92-1'},
            {'name': 'Cadmium (Cd)', 'cas': '7440-43-9'},
            {'name': 'Mercury (Hg)', 'cas': '7439-97-6'},
            {'name': 'Hexavalent Chromium', 'cas': '18540-29-9'},
            {'name': 'Polybrominated Biphenyls (PBB)', 'cas': '59536-65-1'},
            {'name': 'Polybrominated Diphenyl Ethers (PBDE)', 'cas': '1163-19-5'},
            {'name': 'Asbestos', 'cas': '1332-21-4'},
            {'name': 'Polychlorinated Biphenyls (PCB)', 'cas': '1336-36-3'},
            {'name': 'Tributyltin (TBT)', 'cas': '688-73-3'},
            {'name': 'Zinc Compounds', 'cas': '1314-13-2'},
        ]
        
        hazmat_records = []
        materials_per_declaration = count // len(declarations) if len(declarations) > 0 else 3
        
        for decl in declarations:
            num_materials = random.randint(max(1, materials_per_declaration - 1), materials_per_declaration + 2)
            selected_materials = random.sample(materials, min(num_materials, len(materials)))
            
            for mat in selected_materials:
                # Content percentage between 0.01% and 5%
                content_percentage = Decimal(str(round(random.uniform(0.01, 5.0), 2)))
                
                hm = HazardousMaterial.objects.create(
                    declaration=decl,
                    material_name=mat['name'],
                    cas_number=mat['cas'],
                    content_percentage=content_percentage,
                    location_in_product=random.choice([
                        'Component coating', 'Base material', 'Surface treatment',
                        'Additive', 'Pigment', 'Binder', 'Corrosion inhibitor'
                    ]),
                    remarks=f'Concentration: {content_percentage}% by weight' if random.choice([True, False]) else ''
                )
                hazmat_records.append(hm)
        
        return hazmat_records
