import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Views
import HomePage from '@/views/HomePage.vue'
import LoginPage from '@/views/LoginPage.vue'
import RegisterPage from '@/views/RegisterPage.vue'
import DashboardPage from '@/views/DashboardPage.vue'

// Purchase Orders
import PurchaseOrdersPage from '@/views/PurchaseOrdersPage.vue'
import PurchaseOrderCreatePage from '@/views/PurchaseOrderCreatePage.vue'
import PurchaseOrderDetailPage from '@/views/PurchaseOrderDetailPage.vue'

// Declaration Requests
import DeclarationRequestsPage from '@/views/DeclarationRequestsPage.vue'
import MyDeclarationRequestsPage from '@/views/MyDeclarationRequestsPage.vue'

// Declarations
import DeclarationsPage from '@/views/DeclarationsPage.vue'
import MyDeclarationsPage from '@/views/MyDeclarationsPage.vue'
import DeclarationCreatePage from '@/views/DeclarationCreatePage.vue'
import DeclarationDetailPage from '@/views/DeclarationDetailPage.vue'
import ShipDeclarationsPage from '@/views/ShipDeclarationsPage.vue'

// Ships
import ShipsPage from '@/views/ShipsPage.vue'
import ShipFormPage from '@/views/ShipFormPage.vue'
import MyShipsPage from '@/views/MyShipsPage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
    meta: { requiresAuth: false, hideForAuth: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage,
    meta: { requiresAuth: false, hideForAuth: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardPage,
    meta: { requiresAuth: true }
  },
  
  // Purchase Orders
  {
    path: '/purchase-orders',
    name: 'PurchaseOrders',
    component: PurchaseOrdersPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/purchase-orders/new',
    name: 'PurchaseOrderCreate',
    component: PurchaseOrderCreatePage,
    meta: { requiresAuth: true }
  },
  {
    path: '/purchase-orders/:id',
    name: 'PurchaseOrderDetail',
    component: PurchaseOrderDetailPage,
    meta: { requiresAuth: true }
  },
  
  // Declaration Requests
  {
    path: '/declaration-requests',
    name: 'DeclarationRequests',
    component: DeclarationRequestsPage,
    meta: { requiresAuth: true, requiresRole: 'operator' }
  },
  {
    path: '/my-declaration-requests',
    name: 'MyDeclarationRequests',
    component: MyDeclarationRequestsPage,
    meta: { requiresAuth: true, requiresRole: 'supplier' }
  },
  
  // Declarations
  {
    path: '/declarations',
    name: 'Declarations',
    component: DeclarationsPage,
    meta: { requiresAuth: true, requiresRole: 'operator' }
  },
  {
    path: '/my-declarations',
    name: 'MyDeclarations',
    component: MyDeclarationsPage,
    meta: { requiresAuth: true, requiresRole: 'supplier' }
  },
  {
    path: '/declarations/new',
    name: 'DeclarationCreate',
    component: DeclarationCreatePage,
    meta: { requiresAuth: true, requiresRole: 'supplier' }
  },
  {
    path: '/declarations/:id',
    name: 'DeclarationDetail',
    component: DeclarationDetailPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/ship-declarations',
    name: 'ShipDeclarations',
    component: ShipDeclarationsPage,
    meta: { requiresAuth: true, requiresRole: 'customer' }
  },
  
  // Ships
  {
    path: '/ships',
    name: 'Ships',
    component: ShipsPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/ships/new',
    name: 'ShipCreate',
    component: ShipFormPage,
    meta: { requiresAuth: true, requiresRole: 'customer' }
  },
  {
    path: '/ships/:id/edit',
    name: 'ShipEdit',
    component: ShipFormPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/my-ships',
    name: 'MyShips',
    component: MyShipsPage,
    meta: { requiresAuth: true, requiresRole: 'customer' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation Guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const hideForAuth = to.matched.some(record => record.meta.hideForAuth)
  const requiresRole = to.meta.requiresRole
  const isAuthenticated = authStore.isAuthenticated

  if (requiresAuth && !isAuthenticated) {
    // 인증이 필요한 페이지인데 로그인하지 않은 경우
    next('/login')
  } else if (hideForAuth && isAuthenticated) {
    // 로그인/회원가입 페이지인데 이미 로그인한 경우
    next('/dashboard')
  } else if (requiresRole && authStore.userType !== requiresRole) {
    // 역할 기반 접근 제어
    next('/dashboard')
  } else {
    next()
  }
})

export default router
