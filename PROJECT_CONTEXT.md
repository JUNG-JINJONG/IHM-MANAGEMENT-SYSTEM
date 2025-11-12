# IHM Management System - Project Context

## 프로젝트 개요
- **프로젝트명**: IHM (Inventory of Hazardous Materials) Management System
- **목적**: 선박 자재 구매 주문 및 유해물질 신고서 관리 시스템
- **기술 스택**:
  - Backend: Django 5.2.8 + Django REST Framework + JWT Authentication
  - Frontend: Vue 3 + Vite 7.2.2 + Pinia + Vue Router 4
  - Database: MySQL (Railway)
  - Servers: Django :8000, Vue :5173 (또는 :5174)

## 사용자 유형 및 권한
1. **operator (운영자)**: 전체 시스템 관리, 신고서 승인/거절
2. **supplier (공급업체)**: 구매 주문 조회, 신고서 작성 및 제출
3. **customer (고객사/선주)**: 선박 관리, 자신의 선박 관련 주문/신고서 조회

**테스트 계정**:
- operator / password123
- supplier1 / password123
- customer1 / password123

## 데이터베이스 모델 구조

### 1. PurchaseOrder (구매 주문)
**필드 목록** (백엔드 모델 기준 - Single Source of Truth):
- `id`: BigAutoField (PK)
- `ship`: ForeignKey to Ship (필수)
- `supplier`: ForeignKey to Supplier (필수)
- `order_number`: CharField(100, unique=True) - 주문번호 (필수)
- `title`: CharField(200) - 제목 (필수) ✅ **2025-11-12 추가됨**
- `item_name`: CharField(200) - 품목명 (선택) ✅ **2025-11-12 optional로 변경**
- `item_description`: TextField - 품목 설명 (선택)
- `quantity`: DecimalField(10,2) - 수량 (선택) ✅ **2025-11-12 optional로 변경**
- `unit`: CharField(50) - 단위 (선택) ✅ **2025-11-12 optional로 변경**
- `order_date`: DateField - 주문일 (필수)
- `delivery_date`: DateField - 납품일 (선택)
- `status`: CharField(20) - 상태 (pending/requested/completed)
- `created_by`: ForeignKey to User
- `created_at`, `updated_at`: DateTimeField

**중요**: 
- ❌ `po_number`, `total_amount`, `payment_terms`, `notes` 필드는 존재하지 않음
- ⚠️ 품목 상세 정보(item_name, quantity, unit)는 운영자가 구매주문 생성 시 입력하지 않고, 공급업체가 신고서 작성 시 입력

### 2. DeclarationRequest (신고서 요청)
**필드 목록**:
- `id`: BigAutoField (PK)
- `purchase_order`: OneToOneField to PurchaseOrder (필수)
- `supplier`: ForeignKey to Supplier (필수)
- `request_date`: DateField (auto_now_add)
- `due_date`: DateField - 마감일 (선택)
- `status`: CharField(20) - 상태 (pending/submitted/approved/rejected)
- `created_by`: ForeignKey to User
- `created_at`, `updated_at`: DateTimeField

**중요**: ❌ `notes`, `required_date` 필드는 존재하지 않음

### 3. Declaration (신고서)
**필드 목록**:
- `id`: BigAutoField (PK)
- `declaration_request`: OneToOneField to DeclarationRequest (필수)
- `supplier`: ForeignKey to Supplier (필수)
- `ship`: ForeignKey to Ship (필수)
- `declaration_type`: CharField(10) - 'MD' or 'SDoC'
- `item_name`: CharField(200)
- `manufacturer`, `model_number`: CharField
- `hazardous_materials_json`: JSONField
- `compliance_status`: CharField(20) - compliant/non_compliant
- `certification_number`: CharField(100)
- `supplier_signature`, `supplier_name`: CharField
- `signature_date`: DateField
- `submitted_date`, `approved_date`: DateTimeField
- `approved_by`: ForeignKey to User
- `status`: CharField(20) - draft/submitted/approved/rejected
- `rejection_reason`: TextField
- `created_at`, `updated_at`: DateTimeField

### 4. Ship (선박)
**필드 목록**:
- `id`, `customer`, `ship_name`, `imo_number`, `ship_type`, `gross_tonnage`, `year_built`, `is_active`, `created_at`, `updated_at`

### 5. Supplier (공급업체)
**필드 목록**:
- `id`, `user`, `company_name`, `business_number`, `address`, `contact_person`, `contact_phone`, `contact_email`, `created_at`, `updated_at`

## API 엔드포인트 (올바른 경로)

### 백엔드 URL 구조:
- `/api/token/` - JWT 토큰 발급
- `/api/token/refresh/` - JWT 토큰 갱신
- `/api/purchase-orders/` - 구매 주문 CRUD
- `/api/declaration-requests/` - 신고서 요청 CRUD
  - `/api/declaration-requests/{id}/approve/` - 승인 (POST)
  - `/api/declaration-requests/{id}/reject/` - 거절 (POST)
- `/api/declarations/` - 신고서 CRUD
  - `/api/declarations/{id}/approve/` - 승인 (POST)
  - `/api/declarations/{id}/reject/` - 거절 (POST)
- `/api/ships/` - 선박 CRUD
- `/api/users/suppliers/` - 공급업체 목록

**잘못된 경로 (사용하지 말 것)**:
- ❌ `/ships/purchase-orders/`
- ❌ `/ships/ships/`
- ❌ `/declarations/declaration-requests/`

## 최근 주요 변경사항 (2025-11-12)

### ✅ 완료된 작업:

1. **PurchaseOrder 모델 title 필드 추가**
   - Migration: 0003_purchaseorder_title.py
   - CharField(max_length=200, verbose_name='제목')
   - Serializer 업데이트 완료

2. **PurchaseOrder 품목 정보 필드 optional로 변경** ⭐ NEW
   - Migration: 0004_alter_purchaseorder_item_name_and_more.py
   - `item_name`, `quantity`, `unit` 필드를 blank=True, null=True로 변경
   - 운영자는 구매주문 생성 시 기본 정보만 입력 (제목, 선박, 공급업체)
   - 품목 상세 정보는 공급업체가 신고서 작성 시 입력하도록 변경

3. **구매 주문 생성 폼 간소화** ⭐ NEW
   - 백엔드 모델에 맞게 필드 완전히 수정
   - 운영자 입력 항목:
     - `order_number` (자동생성, disabled)
     - `order_date` (오늘 날짜, disabled)
     - `title` (필수)
     - `ship` (선택)
     - `supplier` (선택, 공급업체 목록 로드)
   - 제거된 항목: `item_name`, `quantity`, `unit`, `item_description`, `delivery_date`
   - 도움말 추가: "품목 상세 정보는 공급업체가 신고서 작성 시 입력합니다."

3. **네비게이션 레이아웃 변경**
   - 왼쪽 사이드바 → 상단 1행 수평 메뉴로 변경
   - 반응형: 1024px 이하에서 텍스트 숨김

4. **프론트엔드 필드명 통일**
   - `po_number` → `order_number`
   - `required_date` → `due_date`
   - `total_amount`, `payment_terms`, `notes` 제거 (백엔드에 없음)

5. **API 엔드포인트 경로 수정**
   - ShipFormPage: `/ships/ships/` → `/ships/`
   - DeclarationRequestsPage: `/declarations/declaration-requests/` → `/declaration-requests/`

6. **백엔드 ViewSet 액션 추가**
   - DeclarationRequestViewSet에 approve(), reject() 액션 추가

7. **한글화 작업**
   - PurchaseOrderCreate, MyDeclarationRequests, MyDeclarations, MyShips, ShipDeclarations 페이지
   - 상태 필터 레이블 한글화

## 개발 원칙

### ⚠️ 중요: 백엔드 우선 원칙
1. **백엔드 모델이 Single Source of Truth**
2. 새 기능 추가 순서:
   - ① 백엔드 모델 정의 → 마이그레이션
   - ② Serializer fields 정의
   - ③ 프론트엔드에서 Serializer fields를 참조하여 구현
3. 프론트엔드와 백엔드 필드 불일치 발생 시 → **백엔드를 기준으로 수정**

### 코드 스타일
- 백엔드: Django 기본 스타일, snake_case
- 프론트엔드: Vue 3 Composition API, camelCase
- 한글 레이블 및 메시지 사용

## 알려진 이슈 및 TODO

### 현재 이슈:
- PurchaseOrderDetailPage.vue는 아직 구식 필드(`po_number`, `total_amount` 등) 사용 중
  - 이 페이지는 복잡도가 높아 수정 보류
  - 필요 시 백엔드 기준으로 완전 재작성 필요

### TODO:
- [ ] PurchaseOrderDetailPage.vue 리팩토링
- [ ] TypeScript 도입 고려 (타입 안정성 향상)
- [ ] API 통합 테스트 추가
- [ ] Swagger/OpenAPI 문서 생성

## 실행 방법
```bash
# 백엔드 실행
cd c:\projects\IHM-MANAGEMENT-SYSTEM
python manage.py runserver  # http://localhost:8000

# 프론트엔드 실행
cd c:\projects\IHM-MANAGEMENT-SYSTEM\ihm-frontend
npm run dev  # http://localhost:5173 (또는 5174)
```

## 마이그레이션 히스토리
- 0001_initial.py - 초기 모델 생성 (2025-11-11)
- 0002_initial.py - 관계 설정
- 0003_purchaseorder_title.py - PurchaseOrder title 필드 추가 (2025-11-12)
- 0004_alter_purchaseorder_item_name_and_more.py - PurchaseOrder 품목 필드 optional로 변경 (2025-11-12)

---
**마지막 업데이트**: 2025-11-12 15:30
**작성자**: AI Assistant와 협업 개발
