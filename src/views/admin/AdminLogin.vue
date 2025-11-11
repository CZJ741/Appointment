<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-primary/90 to-primary-dark">
    <div class="max-w-md w-full space-y-8 bg-white rounded-xl shadow-2xl p-8">
      <!-- 返回首页按钮 -->
      <div class="text-left">
        <router-link 
          to="/" 
          class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors duration-200"
        >
          <svg class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          返回首页
        </router-link>
      </div>
      
      <!-- Logo和标题 -->
      <div class="text-center">
        <div class="inline-block p-3 bg-primary rounded-lg mb-4">
          <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <h2 class="text-3xl font-extrabold text-gray-900">管理员登录</h2>
        <p class="mt-2 text-sm text-gray-600">请输入您的管理员凭据</p>
      </div>

      <!-- 登录表单 -->
      <form @submit.prevent="handleLogin" class="mt-8 space-y-6">
        <!-- 用户名 -->
        <div class="rounded-md -space-y-px">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 mb-1">用户名</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <input
                id="username"
                v-model="form.username"
                type="text"
                required
                class="appearance-none rounded-none relative block w-full pl-10 pr-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-primary focus:border-primary sm:text-sm transition-all duration-200"
                placeholder="请输入用户名"
                :class="{ 'border-red-500 focus:ring-red-500 focus:border-red-500': errors.username }"
              />
            </div>
            <p v-if="errors.username" class="mt-1 text-xs text-red-600">{{ errors.username }}</p>
          </div>

          <!-- 密码 -->
          <div class="mt-5">
            <label for="password" class="block text-sm font-medium text-gray-700 mb-1">密码</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="appearance-none rounded-none relative block w-full pl-10 pr-10 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-primary focus:border-primary sm:text-sm transition-all duration-200"
                placeholder="请输入密码"
                :class="{ 'border-red-500 focus:ring-red-500 focus:border-red-500': errors.password }"
              />
              <button
                type="button"
                @click="togglePasswordVisibility"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path v-if="!showPassword" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path v-if="!showPassword" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  <path v-if="showPassword" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.568-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                </svg>
              </button>
            </div>
            <p v-if="errors.password" class="mt-1 text-xs text-red-600">{{ errors.password }}</p>
          </div>

          <!-- 验证码 -->
          <div class="mt-5">
            <label for="captcha" class="block text-sm font-medium text-gray-700 mb-1">验证码</label>
            <div class="flex space-x-3">
              <div class="relative flex-grow">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <input
                  id="captcha"
                  v-model="form.captcha"
                  type="text"
                  required
                  class="appearance-none rounded-none relative block w-full pl-10 pr-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-primary focus:border-primary sm:text-sm transition-all duration-200"
                  placeholder="请输入验证码"
                  :class="{ 'border-red-500 focus:ring-red-500 focus:border-red-500': errors.captcha }"
                />
              </div>
              <div class="w-32 h-12 bg-gray-100 rounded-md flex items-center justify-center text-gray-800 font-mono text-sm cursor-pointer relative overflow-hidden">
                <!-- 验证码图像 (模拟) -->
                <div class="absolute inset-0 flex items-center justify-center" @click="refreshCaptcha">
                  <div class="text-center">
                    <div class="transform -rotate-3">{{ captchaText[0] }}</div>
                    <div class="transform rotate-1">{{ captchaText[1] }}</div>
                    <div class="transform -rotate-2">{{ captchaText[2] }}</div>
                    <div class="transform rotate-3">{{ captchaText[3] }}</div>
                  </div>
                </div>
                <!-- 干扰线 -->
                <svg v-for="i in 3" :key="i" class="absolute inset-0 w-full h-full text-gray-300">
                  <path :d="getRandomPath()" stroke="currentColor" stroke-width="1" fill="none" />
                </svg>
              </div>
            </div>
            <p v-if="errors.captcha" class="mt-1 text-xs text-red-600">{{ errors.captcha }}</p>
          </div>
        </div>

        <!-- 错误提示 -->
        <div v-if="loginError" class="bg-red-50 border border-red-200 rounded-md p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm text-red-700">{{ loginError }}</p>
            </div>
          </div>
        </div>

        <!-- 记住我选项 -->
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input
              id="remember-me"
              v-model="form.rememberMe"
              type="checkbox"
              class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
            />
            <label for="remember-me" class="ml-2 block text-sm text-gray-900">记住我</label>
          </div>
          <div class="text-sm">
            <a href="#" class="font-medium text-primary hover:text-primary-dark transition-colors duration-200">忘记密码?</a>
          </div>
        </div>

        <!-- 登录按钮 -->
        <div>
          <button
            type="submit"
            :disabled="loading"
            class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all duration-200 disabled:opacity-70 disabled:cursor-not-allowed"
          >
            <span v-if="!loading" class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg class="h-5 w-5 text-white group-hover:text-gray-100 transition-colors duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3v-1m3 0h14m-6 4h4m-6 0h2m-2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </span>
            <span v-if="loading" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              登录中...
            </span>
            <span v-else>管理员登录</span>
          </button>
        </div>
      </form>

      <!-- 页脚信息 -->
      <div class="mt-8 border-t border-gray-200 pt-4 text-center">
        <p class="text-sm text-gray-500">
          &copy; {{ new Date().getFullYear() }} 戒毒人员亲属探访预约系统 - 管理后台
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import notification from '../../utils/notification.js'
import { generateCaptcha as generateAuthCaptcha, validateAdminLogin } from '../../utils/auth.js'

export default {
  name: 'AdminLogin',
  setup() {
    const store = useStore()
    const router = useRouter()
    const loading = ref(false)
    const showPassword = ref(false)
    const captchaText = ref('')
    const loginError = ref('')
    
    // 表单数据
    const form = ref({
      username: '',
      password: '',
      captcha: '',
      rememberMe: false
    })
    
    // 表单验证错误
    const errors = ref({
      username: '',
      password: '',
      captcha: ''
    })

    // 生成验证码
    const generateCaptcha = () => {
      captchaText.value = generateAuthCaptcha()
    }

    // 刷新验证码
    const refreshCaptcha = () => {
      generateCaptcha()
    }

    // 生成随机路径
    const getRandomPath = () => {
      const x1 = Math.random() * 128
      const y1 = Math.random() * 48
      const x2 = Math.random() * 128
      const y2 = Math.random() * 48
      return `M${x1},${y1} C${x1 + Math.random() * 50},${y1} ${x2},${y2 - Math.random() * 50} ${x2},${y2}`
    }

    // 验证表单
    const validateForm = () => {
      let isValid = true
      
      // 重置错误
      errors.value = {
        username: '',
        password: '',
        captcha: ''
      }
      
      // 验证用户名
      if (!form.value.username.trim()) {
        errors.value.username = '请输入用户名'
        isValid = false
      }
      
      // 验证密码
      if (!form.value.password.trim()) {
        errors.value.password = '请输入密码'
        isValid = false
      } else if (form.value.password.length < 6) {
        errors.value.password = '密码长度不能少于6位'
        isValid = false
      }
      
      // 验证验证码
      if (!form.value.captcha.trim()) {
        errors.value.captcha = '请输入验证码'
        isValid = false
      }
      
      return isValid
    }

    // 处理登录
    const handleLogin = async () => {
      // 清除之前的错误
      loginError.value = ''
      
      // 验证表单
      if (!validateForm()) {
        return
      }
      
      loading.value = true
      
      try {
        // 使用身份验证工具验证登录
        const result = validateAdminLogin(form.value.username, form.value.password, form.value.captcha)
        
        if (result.success) {
          // 更新Vuex状态
          await store.dispatch('adminLogin', {
            username: form.value.username,
            password: form.value.password
          })
          
          notification.success('登录成功', '欢迎回来，' + result.user.name)
          // 登录成功，跳转到管理面板
          router.push('/admin/dashboard')
        } else {
          notification.error(result.message)
          // 刷新验证码
          refreshCaptcha()
          form.value.captcha = ''
        }
      } catch (error) {
        notification.error('登录失败，请稍后重试')
        console.error('Login error:', error)
      } finally {
        loading.value = false
      }
    }

    // 切换密码可见性
    const togglePasswordVisibility = () => {
      showPassword.value = !showPassword.value
    }
    
    // 处理回车键登录
    const handleKeyPress = (event) => {
      if (event.key === 'Enter') {
        handleLogin()
      }
    }

    // 组件挂载时生成验证码
    onMounted(() => {
      generateCaptcha()
      
      // 检查是否已登录
      if (store.state.isAdminLoggedIn) {
        router.push('/admin/dashboard')
      }
      
      // 聚焦用户名输入框
      document.getElementById('username')?.focus()
    })

    return {
      form,
      errors,
      loading,
      showPassword,
      captchaText,
      loginError,
      validateForm,
      handleLogin,
      togglePasswordVisibility,
      refreshCaptcha,
      getRandomPath,
      handleKeyPress
    }
  }
}
</script>

<style scoped>
/* 自定义动画 */
@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-5px); }
  100% { transform: translateY(0px); }
}

/* 验证码文字样式 */
.text-center > div {
  position: absolute;
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.text-center > div:nth-child(1) {
  left: 25%;
  top: 35%;
  color: #1E40AF;
  animation: float 3s ease-in-out infinite;
}

.text-center > div:nth-child(2) {
  left: 40%;
  top: 45%;
  color: #059669;
  animation: float 3.5s ease-in-out infinite 0.5s;
}

.text-center > div:nth-child(3) {
  left: 55%;
  top: 35%;
  color: #DC2626;
  animation: float 4s ease-in-out infinite 1s;
}

.text-center > div:nth-child(4) {
  left: 70%;
  top: 45%;
  color: #D97706;
  animation: float 3.8s ease-in-out infinite 1.5s;
}

/* 输入框聚焦动画 */
input:focus {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 按钮悬停效果 */
button:enabled:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

button:active {
  transform: translateY(0);
}
</style>