import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'

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
      component: () => import('../views/visitor/BookingPage.vue')
    },
    {
      path: '/appointments',
      name: 'appointments',
      component: () => import('../views/visitor/AppointmentsPage.vue')
    },
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
  const isAuthenticated = localStorage.getItem('admin_token')
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next({ name: 'adminLogin' })
  } else {
    next()
  }
})

export default router