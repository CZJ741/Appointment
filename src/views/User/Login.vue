<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          探访人登录
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          请登录以预约探访
        </p>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="rounded-md -space-y-px">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 mb-1">
              用户名
            </label>
            <input
              id="username"
              name="username"
              type="text"
              autocomplete="username"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm"
              placeholder="请输入用户名"
              v-model="form.username"
            />
          </div>
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-1">
              密码
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autocomplete="current-password"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm"
              placeholder="请输入密码"
              v-model="form.password"
            />
          </div>
        </div>

        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input
              id="remember-me"
              name="remember-me"
              type="checkbox"
              class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
              v-model="form.rememberMe"
            />
            <label for="remember-me" class="ml-2 block text-sm text-gray-900">
              记住我
            </label>
          </div>

          <!-- <div class="text-sm">
            <a href="#" class="font-medium text-primary hover:text-primary-dark">
              忘记密码？
            </a>
          </div> -->
        </div>

        <div>
          <button
            type="submit"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            :disabled="isLoading"
          >
            <span v-if="isLoading" class="inline-flex items-center">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              登录中...
            </span>
            <span v-else>登录</span>
          </button>
        </div>

        <div class="text-center text-sm">
          <span class="text-gray-600">还没有账号？</span>
          <router-link to="/user/register" class="font-medium text-primary hover:text-primary-dark ml-1">
            立即注册
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import notification from '@/utils/notification.js'
import axios from 'axios'

export default {
  name: 'UserLogin',
  setup() {
    const router = useRouter()
    const store = useStore()
    const isLoading = ref(false)
    const form = ref({
      username: '',
      password: '',
      rememberMe: false
    })

    const handleLogin = async () => {
      if (!form.value.username || !form.value.password) {
        notification.warning('请填写完整信息', '登录提示')
        return
      }

      isLoading.value = true
      try {
        // 使用store中的login action进行登录
        const result = await store.dispatch('userLogin', form.value)
        
        if (result && result.success) {
          notification.success('登录成功', '欢迎回来')
          // 跳转到首页
          router.push('/')
        } else {
          notification.error('登录失败', '请检查用户名和密码')
        }
      } catch (error) {
        console.error('登录错误:', error)
        notification.error('登录失败', error.message || '请稍后重试')
      } finally {
        isLoading.value = false
      }
    }

    const goToRegister = () => {
      router.push('/user/register')
    }

    return {
      form,
      isLoading,
      handleLogin,
      goToRegister
    }
  }
}
</script>

<style scoped>
/* 主色调变量 */
:root {
  --primary-color: #4f46e5;
  --primary-dark-color: #4338ca;
}

/* 表单样式增强 */
input:focus-within {
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2) !important;
}

/* 按钮悬停效果 */
.group:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.group:active {
  transform: translateY(0);
}

/* 加载动画 */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>