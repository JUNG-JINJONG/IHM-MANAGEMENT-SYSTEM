# IHM Management System - Frontend 완성

## 구현된 핵심 기능

### 1. 공통 컴포넌트 (5개)
✅ **DataTable.vue** - 페이지네이션, 정렬, 커스텀 셀 렌더링
✅ **Modal.vue** - 재사용 가능한 모달 다이얼로그
✅ **LoadingSpinner.vue** - 로딩 표시
✅ **ConfirmDialog.vue** - 확인/취소 다이얼로그
✅ **FormInput.vue** - 통합 폼 입력 컴포넌트 (text, textarea, select, date, file)

### 2. Purchase Orders (4개 페이지)
✅ **PurchaseOrdersPage.vue** - 구매주문 목록 (검색, 필터링, 페이지네이션)
✅ **PurchaseOrderCreatePage.vue** - 새 구매주문 생성
✅ **PurchaseOrderDetailPage.vue** - 구매주문 상세/수정, 신고서 요청 버튼
✅ Request Declaration Modal - 구매주문에서 직접 신고서 요청

### 3. Declaration Requests (2개 페이지)
✅ **DeclarationRequestsPage.vue** - 운영자용: 모든 신고서 요청 관리, 승인/거부
✅ **MyDeclarationRequestsPage.vue** - 공급업체용: 내 신고서 요청 확인, 신고서 작성

### 4. Declarations (5개 페이지)
✅ **DeclarationsPage.vue** - 운영자용: 탭으로 상태별 신고서 관리
✅ **MyDeclarationsPage.vue** - 공급업체용: 내가 작성한 신고서
✅ **DeclarationCreatePage.vue** - MD/SDoC 선택, 유해물질 동적 추가
✅ **DeclarationDetailPage.vue** - 상세 정보, 유해물질 목록, 승인/거부
✅ **ShipDeclarationsPage.vue** - 고객사용: 선박별 신고서 조회

### 5. Ships (4개 페이지)
✅ **ShipsPage.vue** - 모든 선박 목록
✅ **ShipFormPage.vue** - 선박 생성/수정 (동일 컴포넌트)
✅ **MyShipsPage.vue** - 고객사용: 내 선박 목록
✅ Declaration 연동 - 선박별 신고서 바로 조회

### 6. 라우팅 및 권한
✅ **router/index.js** - 모든 라우트 구성 완료
✅ 역할 기반 접근 제어 (operator, supplier, customer)
✅ 인증 가드 (requiresAuth, hideForAuth)
✅ **Sidebar.vue** - 역할별 메뉴 표시

## 주요 기능

### 워크플로우
1. **공급업체**: 구매주문 생성 → 신고서 요청 → 신고서 작성 → 제출
2. **운영자**: 신고서 요청 승인 → 제출된 신고서 검토 → 승인/거부
3. **고객사**: 내 선박 조회 → 선박별 신고서 확인

### UI/UX 특징
- 일관된 디자인 시스템 (색상, 간격, 타이포그래피)
- 반응형 그리드 레이아웃
- 상태별 배지 색상 구분
- 실시간 검색 (500ms debounce)
- 페이지네이션
- 로딩 상태 표시
- 에러 핸들링

### API 연동
- RESTful API 호출
- JWT 토큰 자동 갱신
- 역할 기반 데이터 필터링
- Nested serializer 활용 (관계 데이터 포함)

## 파일 구조

```
ihm-frontend/
├── src/
│   ├── components/
│   │   ├── DataTable.vue
│   │   ├── Modal.vue
│   │   ├── LoadingSpinner.vue
│   │   ├── ConfirmDialog.vue
│   │   ├── FormInput.vue
│   │   ├── Navbar.vue
│   │   ├── Sidebar.vue
│   │   └── AppLayout.vue
│   ├── views/
│   │   ├── HomePage.vue
│   │   ├── LoginPage.vue
│   │   ├── RegisterPage.vue
│   │   ├── DashboardPage.vue
│   │   ├── PurchaseOrdersPage.vue
│   │   ├── PurchaseOrderCreatePage.vue
│   │   ├── PurchaseOrderDetailPage.vue
│   │   ├── DeclarationRequestsPage.vue
│   │   ├── MyDeclarationRequestsPage.vue
│   │   ├── DeclarationsPage.vue
│   │   ├── MyDeclarationsPage.vue
│   │   ├── DeclarationCreatePage.vue
│   │   ├── DeclarationDetailPage.vue
│   │   ├── ShipDeclarationsPage.vue
│   │   ├── ShipsPage.vue
│   │   ├── ShipFormPage.vue
│   │   └── MyShipsPage.vue
│   ├── stores/
│   │   └── auth.js
│   ├── services/
│   │   └── api.js
│   ├── router/
│   │   └── index.js
│   ├── App.vue
│   └── main.js
```

## 다음 단계 (선택사항)

1. **에러 처리 개선**: Toast 알림 시스템 추가
2. **검증 강화**: Form validation 라이브러리 (예: Vuelidate)
3. **테스트**: Unit tests, E2E tests
4. **최적화**: Code splitting, Lazy loading
5. **추가 기능**: 
   - 파일 업로드/다운로드
   - PDF 생성
   - 차트/통계
   - 알림 시스템

## 실행 방법

```bash
# 프론트엔드 실행
cd ihm-frontend
npm run dev

# 백엔드 실행 (별도 터미널)
cd ..
python manage.py runserver
```

접속: http://localhost:5173

## 역할별 테스트 계정 (더미 데이터 생성 후)

- **운영자**: operator@test.com
- **공급업체**: supplier@test.com
- **고객사**: customer@test.com

비밀번호: test1234

---

**구현 완료일**: 2025년 11월 11일
**총 페이지 수**: 18개
**총 컴포넌트 수**: 8개
**개발 시간**: ~2시간 (AI 기준)
