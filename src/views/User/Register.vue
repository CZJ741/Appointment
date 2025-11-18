<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          探访人注册
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          创建账号以预约探访
        </p>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div class="space-y-4">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 mb-1">
              用户名
            </label>
            <input
              id="username"
              name="username"
              type="text"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm"
              placeholder="请输入用户名（2-20个字符）"
              v-model="form.username"
            />
          </div>
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
              邮箱
            </label>
            <input
              id="email"
              name="email"
              type="email"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm"
              placeholder="请输入邮箱地址"
              v-model="form.email"
            />
          </div>
          <div>
            <label for="full_name" class="block text-sm font-medium text-gray-700 mb-1">
              姓名
            </label>
            <input
              id="full_name"
              name="full_name"
              type="text"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm"
              placeholder="请输入您的真实姓名"
              v-model="form.full_name"
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
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm"
              placeholder="请输入密码（至少6个字符）"
              v-model="form.password"
            />
          </div>
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1">
              确认密码
            </label>
            <input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm"
              placeholder="请再次输入密码"
              v-model="form.confirmPassword"
            />
          </div>
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
              注册中...
            </span>
            <span v-else>注册</span>
          </button>
        </div>

        <div class="text-center text-sm">
          <span class="text-gray-600">已有账号？</span>
          <router-link to="/user/login" class="font-medium text-primary hover:text-primary-dark ml-1">
            立即登录
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import notification from '@/utils/notification.js'

const router = useRouter()
const isLoading = ref(false)

// 使用reactive更好地管理表单数据
const form = reactive({
  username: '',
  email: '',
  full_name: '',
  password: '',
  confirmPassword: ''
})

const validateForm = () => {
  // 验证用户名
  if (!form.username || form.username.length < 2 || form.username.length > 20) {
    notification.warning('用户名长度应为2-20个字符', '验证失败')
    return false
  }

  // 验证邮箱
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!form.email || !emailRegex.test(form.email)) {
    notification.warning('请输入有效的邮箱地址', '验证失败')
    return false
  }

  // 验证姓名
  if (!form.full_name || form.full_name.trim().length < 2) {
    notification.warning('请输入有效的姓名', '验证失败')
    return false
  }

  // 验证密码
  if (!form.password || form.password.length < 6) {
    notification.warning('密码长度至少为6个字符', '验证失败')
    return false
  }

  // 验证密码一致性
  if (form.password !== form.confirmPassword) {
    notification.warning('两次输入的密码不一致', '验证失败')
    return false
  }

  return true
}

const handleRegister = async () => {
  if (!validateForm()) {
    return
  }

  isLoading.value = true
  try {
    // 调用后端API进行注册
    const response = await fetch('/api/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: form.username,
        email: form.email,
        full_name: form.full_name,
        password: form.password,
        password_confirm: form.confirmPassword
      })
    })
    
    const data = await response.json()
    
    if (response.ok) {
      notification.success('注册成功', '请登录')
      // 跳转到登录页面，添加查询参数
      router.push({
        path: '/user/login',
        query: { registered: 'true' }
      })
    } else {
      // 处理验证错误
      if (data.error && typeof data.error === 'object') {
        // 如果错误是对象形式
        const errorMessages = []
        for (const field in data.error) {
          errorMessages.push(`${field}: ${data.error[field].join(', ')}`)
        }
        notification.error('注册失败', errorMessages.join('; '))
      } else {
        notification.error('注册失败', data.error || '请稍后重试')
      }
    }
  } catch (error) {
    console.error('注册错误:', error)
    notification.error('注册失败', '网络错误，请检查您的连接后重试')
  } finally {
    isLoading.value = false
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