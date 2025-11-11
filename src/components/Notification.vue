<template>
  <div 
    v-if="visible" 
    class="fixed top-4 right-4 z-50 max-w-sm w-full bg-white dark:bg-gray-800 shadow-lg rounded-lg overflow-hidden transform transition-all duration-300 ease-in-out"
    :class="notificationClasses"
    :style="notificationStyle"
  >
    <div class="p-4 flex items-start">
      <div class="flex-shrink-0 pt-0.5">
        <svg v-if="type === 'success'" class="h-6 w-6 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        <svg v-else-if="type === 'error'" class="h-6 w-6 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <svg v-else-if="type === 'warning'" class="h-6 w-6 text-yellow-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <svg v-else class="h-6 w-6 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <div class="ml-3 w-0 flex-1 pt-0.5">
        <p class="text-sm font-medium text-gray-900 dark:text-gray-100">
          {{ title }}
        </p>
        <p v-if="message" class="mt-1 text-sm text-gray-500 dark:text-gray-400">
          {{ message }}
        </p>
      </div>
      <div class="ml-4 flex-shrink-0 flex">
        <button 
          @click="close"
          class="bg-white rounded-md inline-flex text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        >
          <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
    <!-- 进度条 -->
    <div 
      class="h-1 bg-gray-200 dark:bg-gray-700 overflow-hidden"
      :style="{ opacity: 0.5 + (progress / 100) * 0.5 }"
    >
      <div 
        class="h-full transition-all duration-300 ease-out"
        :class="progressBarClass"
        :style="{ width: progress + '%' }"
      ></div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'

export default {
  name: 'Notification',
  props: {
    type: {
      type: String,
      default: 'info',
      validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
    },
    title: {
      type: String,
      required: true
    },
    message: {
      type: String,
      default: ''
    },
    duration: {
      type: Number,
      default: 5000
    },
    showProgress: {
      type: Boolean,
      default: true
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const visible = ref(false)
    const progress = ref(100)
    let timer = null
    let progressTimer = null

    // 计算样式类
    const notificationClasses = computed(() => {
      return {
        'bg-green-50 border-l-4 border-green-500': props.type === 'success',
        'bg-red-50 border-l-4 border-red-500': props.type === 'error',
        'bg-yellow-50 border-l-4 border-yellow-500': props.type === 'warning',
        'bg-blue-50 border-l-4 border-blue-500': props.type === 'info'
      }
    })

    const progressBarClass = computed(() => {
      const classMap = {
        success: 'bg-green-500',
        error: 'bg-red-500',
        warning: 'bg-yellow-500',
        info: 'bg-blue-500'
      }
      return classMap[props.type] || 'bg-blue-500'
    })

    // 通知样式
    const notificationStyle = computed(() => {
      if (!visible.value) {
        return {
          opacity: 0,
          transform: 'translateX(100%)'
        }
      }
      return {
        opacity: 1,
        transform: 'translateX(0)'
      }
    })

    // 开始计时器
    const startTimer = () => {
      if (props.duration > 0) {
        timer = setTimeout(() => {
          close()
        }, props.duration)

        if (props.showProgress) {
          const step = 100 / (props.duration / 16)
          progressTimer = setInterval(() => {
            progress.value -= step
            if (progress.value <= 0) {
              clearInterval(progressTimer)
            }
          }, 16)
        }
      }
    }

    // 清除计时器
    const clearTimers = () => {
      if (timer) {
        clearTimeout(timer)
        timer = null
      }
      if (progressTimer) {
        clearInterval(progressTimer)
        progressTimer = null
      }
    }

    // 关闭通知
    const close = () => {
      visible.value = false
      clearTimers()
      // 动画结束后触发关闭事件
      setTimeout(() => {
        emit('close')
      }, 300)
    }

    // 鼠标悬停时暂停计时
    const pauseTimer = () => {
      clearTimers()
    }

    // 鼠标离开时继续计时
    const resumeTimer = () => {
      startTimer()
    }

    onMounted(() => {
      // 延迟显示，让父组件可以添加到DOM中
      setTimeout(() => {
        visible.value = true
        startTimer()
      }, 10)
    })

    onUnmounted(() => {
      clearTimers()
    })

    return {
      visible,
      progress,
      notificationClasses,
      progressBarClass,
      notificationStyle,
      close,
      pauseTimer,
      resumeTimer
    }
  }
}
</script>

<style scoped>
/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>