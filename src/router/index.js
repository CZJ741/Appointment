import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import { useStore } from 'vuex'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage
    },
    {
      path: '/booking',
      name: 'booking',
      component: () => import('../views/visitor/BookingPage.vue'),
      meta: { requiresUserAuth: true }
    },
    {
      path: '/appointments',
      name: 'appointments',
      component: () => import('../views/visitor/AppointmentsPage.vue'),
      meta: { requiresUserAuth: true }
    },
    // 用户登录和注册路由
    {
      path: '/user/login',
      name: 'userLogin',
      component: () => import('../views/User/Login.vue')
    },
    {
      path: '/user/register',
      name: 'userRegister',
      component: () => import('../views/User/Register.vue')
    },
    // 管理员路由
    {
      path: '/admin/login',
      name: 'adminLogin',
      component: () => import('../views/admin/AdminLogin.vue')
    },
    {
      path: '/admin/dashboard',
      name: 'adminDashboard',
      component: () => import('../views/admin/Dashboard.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/admin/appointments',
      name: 'adminAppointments',
      component: () => import('../views/admin/AppointmentsList.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/admin/appointment/:id',
      name: 'adminAppointmentDetail',
      component: () => import('../views/admin/AppointmentDetail.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 检查是否需要管理员登录
  const requiresAdminAuth = to.matched.some(record => record.meta.requiresAuth)
  // 检查是否需要用户登录
  const requiresUserAuth = to.matched.some(record => record.meta.requiresUserAuth)
  
  // 管理员登录状态检查
  const isAdminAuthenticated = localStorage.getItem('admin_token')
  
  // 用户登录状态检查
  const isUserAuthenticated = localStorage.getItem('user_token')
  
  if (requiresAdminAuth && !isAdminAuthenticated) {
    // 需要管理员登录但未登录，重定向到管理员登录页
    next({ name: 'adminLogin' })
  } else if (requiresUserAuth && !isUserAuthenticated) {
    // 需要用户登录但未登录，重定向到用户登录页
    next({ name: 'userLogin' })
  } else {
    // 允许访问
    next()
  }
})

export default router