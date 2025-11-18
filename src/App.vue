<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <!-- 全局导航栏 -->
    <nav v-if="!isAdminLoginPage" class="bg-white shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <span class="text-xl font-bold text-primary">戒毒人员亲属探访预约系统</span>
            </div>
          </div>
          <div class="flex items-center">
            <!-- 普通用户导航 -->
            <div v-if="!isAdminRoute" class="hidden md:block">
              <div class="ml-10 flex items-baseline space-x-4">
                <router-link
                  to="/"
                  class="nav-link"
                  active-class="nav-link-active"
                >
                  首页
                </router-link>
                <router-link
                  to="/booking"
                  class="nav-link"
                  active-class="nav-link-active"
                  @click="handleProtectedRoute"
                >
                  预约探访
                </router-link>
                <router-link
                  to="/appointments"
                  class="nav-link"
                  active-class="nav-link-active"
                  @click="handleProtectedRoute"
                >
                  我的预约
                </router-link>
              </div>
            </div>
            <!-- 移动端菜单按钮 -->
            <div class="md:hidden">
              <button 
                @click="mobileMenuOpen = !mobileMenuOpen"
                class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:bg-gray-100 focus:text-gray-500"
              >
                <svg class="h-6 w-6" stroke="currentColor" fill="none" viewBox="0 0 24 24">
                  <path :stroke-linecap="mobileMenuOpen ? 'round' : 'round'" :stroke-linejoin="mobileMenuOpen ? 'round' : 'round'" :stroke-width="2" :d="mobileMenuOpen ? 'M6 18L18 6M6 6l12 12' : 'M4 6h16M4 12h16M4 18h16'" />
                </svg>
              </button>
            </div>
            <!-- 用户登录/退出 -->
            <div v-if="!isAdminRoute" class="flex items-center ml-4">
              <button
                v-if="isUserLoggedIn"
                @click="userLogout"
                class="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 transition-colors duration-200"
              >
                退出登录
              </button>
              <router-link
                v-else
                to="/user/login"
                class="px-3 py-2 rounded-md text-sm font-medium text-white bg-primary hover:bg-primary-dark transition-colors duration-200"
              >
                探访人登录
              </router-link>
            </div>
            <!-- 管理员入口 -->
            <router-link 
              v-if="!isAdminRoute" 
              to="/admin/login"
              class="ml-4 px-3 py-2 rounded-md text-sm font-medium text-white bg-gray-600 hover:bg-gray-700 transition-colors duration-200"
            >
              管理员登录
            </router-link>
          </div>
        </div>
      </div>

      <!-- 移动端菜单 -->
      <div v-if="mobileMenuOpen" class="md:hidden">
          <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            <router-link
              to="/"
              class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50"
              @click="mobileMenuOpen = false"
            >
              首页
            </router-link>
            <router-link
              to="/booking"
              class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50"
              @click="() => { handleProtectedRoute(); mobileMenuOpen = false; }"
            >
              预约探访
            </router-link>
            <router-link
              to="/appointments"
              class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50"
              @click="() => { handleProtectedRoute(); mobileMenuOpen = false; }"
            >
              我的预约
            </router-link>
            <button
              v-if="isUserLoggedIn"
              @click="userLogout"
              class="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 transition-colors duration-200"
            >
              退出登录
            </button>
            <router-link
              v-else
              to="/user/login"
              class="block px-3 py-2 rounded-md text-base font-medium text-white bg-primary hover:bg-primary-dark transition-colors duration-200"
              @click="mobileMenuOpen = false"
            >
              探访人登录
            </router-link>
            <router-link
              to="/admin/login"
              class="block px-3 py-2 rounded-md text-base font-medium text-white bg-gray-600 hover:bg-gray-700 transition-colors duration-200"
              @click="mobileMenuOpen = false"
            >
              管理员登录
            </router-link>
          </div>
        </div>
    </nav>

    <!-- 管理员侧边栏 -->
    <div v-if="isAdminRoute && $store.state.isAdminLoggedIn" class="flex">
      <aside class="w-64 bg-gray-800 h-screen fixed left-0 top-0 z-10">
        <div class="p-4 text-white text-center">
          <h2 class="text-xl font-bold">管理员系统</h2>
        </div>
        <nav class="mt-5">
          <router-link
            to="/admin/dashboard"
            class="admin-nav-link"
            active-class="admin-nav-link-active"
          >
            <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
            </svg>
            仪表盘
          </router-link>
          <router-link
            to="/admin/appointments"
            class="admin-nav-link"
            active-class="admin-nav-link-active"
          >
            <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            预约管理
          </router-link>
          <button 
            @click="logout"
            class="admin-nav-link text-red-300 hover:text-red-100 hover:bg-gray-700"
          >
            <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            退出登录
          </button>
        </nav>
      </aside>
      <main class="flex-1 ml-64 p-6">
        <router-view />
      </main>
    </div>

    <!-- 主内容区 -->
    <main v-else class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <router-view />
    </main>

    <!-- 页脚 -->
    <footer v-if="!isAdminRoute" class="bg-white border-t border-gray-200 mt-12">
      <div class="max-w-7xl mx-auto py-6 px-4 overflow-hidden sm:px-6 lg:px-8">
        <p class="text-center text-gray-500 text-sm">
          © {{ currentYear }} 戒毒人员亲属探访预约系统 版权所有
        </p>
      </div>
    </footer>

    <!-- 通知区域会由通知管理器自动填充 -->
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import notification from './utils/notification.js'

export default {
  name: 'App',
  setup() {
    const router = useRouter()
    const store = useStore()
    const mobileMenuOpen = ref(false)

    // 计算当前年份
    const currentYear = computed(() => new Date().getFullYear())

    // 判断是否为管理员登录页面
    const isAdminLoginPage = computed(() => {
      return router.currentRoute.value.path === '/admin/login'
    })

    // 判断是否为管理员路由
    const isAdminRoute = computed(() => {
      return router.currentRoute.value.path.startsWith('/admin')
    })

    // 判断用户是否登录
    const isUserLoggedIn = computed(() => {
      return store.state.user && store.state.user.isLoggedIn
    })

    // 管理员登出
    const logout = () => {
      store.dispatch('adminLogout')
      router.push('/admin/login')
      notification.success('退出成功', '您已成功退出管理员系统')
    }

    // 用户登出
    const userLogout = () => {
      store.dispatch('userLogout')
      notification.success('退出成功', '您已成功退出系统')
    }

    // 处理受保护路由访问
    const handleProtectedRoute = (event) => {
      if (!isUserLoggedIn.value) {
        event?.preventDefault()
        notification.warning('请先登录', '访问提示')
        router.push('/user/login')
      }
    }

    // 初始化数据
    onMounted(() => {
      store.dispatch('initializeData')
      
      // 初始化全局事件监听
      setupGlobalEventListeners()
      
      // 注入全局通知方法
      window.showNotification = (type, title, message = '', duration = 3000) => {
        notification[type](message, title)
      }
    })

    // 设置全局事件监听
    const setupGlobalEventListeners = () => {
      // 键盘快捷键
      document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + ? 显示帮助
        if ((e.ctrlKey || e.metaKey) && e.key === '?') {
          e.preventDefault()
          notification.info('暂无快捷键说明', '键盘快捷键')
        }
      })

      // 页面滚动效果
      window.addEventListener('scroll', () => {
        const scrollY = window.scrollY
        const header = document.querySelector('nav')
        if (header) {
          if (scrollY > 50) {
            header.classList.add('shadow-md')
          } else {
            header.classList.remove('shadow-md')
          }
        }
      })

      // 错误处理
      window.addEventListener('error', (event) => {
        console.error('JavaScript Error:', event.error)
        notification.error('发生了一个错误，请刷新页面重试', '系统错误')
      })

      window.addEventListener('unhandledrejection', (event) => {
        console.error('Unhandled Promise Rejection:', event.reason)
        notification.error('发生了一个错误，请刷新页面重试', '系统错误')
      })
    }

    return {
      mobileMenuOpen,
      currentYear,
      isAdminLoginPage,
      isAdminRoute,
      isUserLoggedIn,
      logout,
      userLogout,
      handleProtectedRoute
    }
  }
}
</script>

<style>
/* 导航链接样式 */
.nav-link {
  @apply px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 transition-colors duration-200;
}

.nav-link-active {
  @apply bg-primary text-white;
}

/* 管理员导航链接样式 */
.admin-nav-link {
  @apply flex items-center px-4 py-3 text-gray-300 hover:bg-gray-700 hover:text-white transition-colors duration-200;
}

.admin-nav-link-active {
  @apply bg-primary text-white;
}

/* 移动端菜单 */
.md\:hidden > div {
  animation: slideDown 0.3s ease-in-out;
}

@keyframes slideDown {
  from { 
    opacity: 0;
    transform: translateY(-10px);
  }
  to { 
    opacity: 1;
    transform: translateY(0);
  }
}

/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 平滑滚动 */
html {
  scroll-behavior: smooth;
}

body {
  font-family: 'Noto Sans SC', sans-serif;
}

/* 工具类 */
.text-shadow {
  text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 加载动画 */
@keyframes spin {
  to { transform: rotate(360deg); }
}

.spinner {
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top: 2px solid white;
  width: 24px;
  height: 24px;
  animation: spin 1s linear infinite;
}
</style>