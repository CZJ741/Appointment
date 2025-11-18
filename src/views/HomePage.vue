<template>
  <div class="min-h-screen flex flex-col">
    <!-- Hero 区域 -->
    <section class="hero-bg py-20 px-4 sm:px-6 lg:px-8">
      <div class="max-w-3xl mx-auto text-center">
        <h1 class="text-4xl md:text-5xl font-bold text-white mb-6 text-shadow">
          戒毒人员亲属探访预约系统
        </h1>
        <!-- 探访人信息显示 -->
        <div v-if="currentUser" class="mb-8 text-white text-lg font-medium">
          当前账号: {{ currentUser.username }} | 姓名: {{ currentUser.full_name }}
        </div>
        <p class="text-xl text-white mb-8 text-shadow">
          便捷、规范、安全的探访预约服务
        </p>
        <div class="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-4">
          <router-link 
            to="/booking"
            class="inline-flex justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary hover:bg-primary-dark transition-colors duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-transform duration-200"
          >
            立即预约
          </router-link>
          <router-link 
            to="/appointments"
            class="inline-flex justify-center px-8 py-3 border border-white text-base font-medium rounded-md text-white bg-transparent hover:bg-white/10 transition-colors duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-transform duration-200"
          >
            查看预约
          </router-link>
        </div>
      </div>
    </section>

    <!-- 预约规则区域 -->
    <section class="py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">预约规则</h2>
          <p class="text-lg text-gray-600">请仔细阅读以下预约规则，确保顺利完成预约</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div class="bg-gray-50 rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow duration-300 transform hover:-translate-y-1 transition-transform duration-200">
            <div class="text-primary mb-4">
              <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">探访时间</h3>
            <p class="text-gray-600">每月第3个星期三为接访日，具体探访时间段将在预约成功后通知</p>
          </div>

          <div class="bg-gray-50 rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow duration-300 transform hover:-translate-y-1 transition-transform duration-200">
            <div class="text-primary mb-4">
              <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">批次限制</h3>
            <p class="text-gray-600">每月一个批次，每批次最多可预约3名亲属信息，请合理安排</p>
          </div>

          <div class="bg-gray-50 rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow duration-300 transform hover:-translate-y-1 transition-transform duration-200">
            <div class="text-primary mb-4">
              <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">预约方式</h3>
            <p class="text-gray-600">采用先到先得取号方式，名额有限，请及时完成预约</p>
          </div>

          <div class="bg-gray-50 rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow duration-300 transform hover:-translate-y-1 transition-transform duration-200">
            <div class="text-primary mb-4">
              <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">预约审核</h3>
            <p class="text-gray-600">提交预约后，工作人员将进行审核，审核结果将在3个工作日内通知</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 预约流程区域 -->
    <section class="py-16 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">预约流程</h2>
          <p class="text-lg text-gray-600">简单几步，轻松完成探访预约</p>
        </div>

        <div class="relative">
          <!-- 连接线 -->
          <div class="hidden md:block absolute h-1 bg-gray-300 top-1/2 left-0 right-0 transform -translate-y-1/2"></div>
          
          <div class="grid grid-cols-1 md:grid-cols-4 gap-8 relative z-10">
            <div class="text-center">
              <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary text-white text-2xl font-bold mb-4 shadow-lg">
                1
              </div>
              <h3 class="text-xl font-semibold mb-2">填写预约信息</h3>
              <p class="text-gray-600">提供探访人信息、关系证明等必要资料</p>
            </div>

            <div class="text-center">
              <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary text-white text-2xl font-bold mb-4 shadow-lg">
                2
              </div>
              <h3 class="text-xl font-semibold mb-2">提交预约申请</h3>
              <p class="text-gray-600">确认信息无误后提交申请，获取预约号</p>
            </div>

            <div class="text-center">
              <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary text-white text-2xl font-bold mb-4 shadow-lg">
                3
              </div>
              <h3 class="text-xl font-semibold mb-2">等待审核</h3>
              <p class="text-gray-600">工作人员审核申请，等待审核结果通知</p>
            </div>

            <div class="text-center">
              <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary text-white text-2xl font-bold mb-4 shadow-lg">
                4
              </div>
              <h3 class="text-xl font-semibold mb-2">按时探访</h3>
              <p class="text-gray-600">审核通过后，按指定时间前往探访</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 常见问题区域 -->
    <section class="py-16 bg-white">
      <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">常见问题</h2>
          <p class="text-lg text-gray-600">解答您在预约过程中可能遇到的问题</p>
        </div>

        <div class="space-y-6">
          <div class="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow duration-300">
            <h3 class="text-xl font-semibold mb-2">Q: 如何确认我的预约状态？</h3>
            <p class="text-gray-600">A: 您可以通过"我的预约"页面查看预约状态，系统也会根据审核结果给您发送通知。</p>
          </div>

          <div class="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow duration-300">
            <h3 class="text-xl font-semibold mb-2">Q: 预约成功后可以更改探访时间吗？</h3>
            <p class="text-gray-600">A: 预约成功后原则上不支持更改探访时间，特殊情况请联系工作人员。</p>
          </div>

          <div class="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow duration-300">
            <h3 class="text-xl font-semibold mb-2">Q: 探访需要携带哪些证件？</h3>
            <p class="text-gray-600">A: 探访时需要携带有效身份证件（身份证、户口本等）以及预约确认信息。</p>
          </div>

          <div class="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow duration-300">
            <h3 class="text-xl font-semibold mb-2">Q: 可以带物品给被探访人吗？</h3>
            <p class="text-gray-600">A: 探访物品需符合相关规定，具体请咨询工作人员，易燃易爆、尖锐物品等禁止带入。</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 联系我们区域 -->
    <section class="py-16 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">联系我们</h2>
          <p class="text-lg text-gray-600">如有疑问，请通过以下方式联系我们</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 text-center">
            <div class="text-primary mb-4">
              <svg class="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">电话咨询</h3>
            <p class="text-gray-600">工作日 9:00-17:00</p>
            <p class="text-gray-800 font-medium mt-2">010-12345678</p>
          </div>

          <div class="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 text-center">
            <div class="text-primary mb-4">
              <svg class="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">现场咨询</h3>
            <p class="text-gray-600">北京市朝阳区某街道某号</p>
            <p class="text-gray-800 font-medium mt-2">接待大厅服务台</p>
          </div>

          <div class="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 text-center">
            <div class="text-primary mb-4">
              <svg class="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 15.546c-.523 0-1.046.151-1.5.454a2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.701 2.701 0 00-1.5-.454M9 6v2m3-2v2m3-2v2M9 3h.01M12 3h.01M15 3h.01M21 21v-7a2 2 0 00-2-2H5a2 2 0 00-2 2v7h18zm-3-9v-2a2 2 0 00-2-2H8a2 2 0 00-2 2v2h12z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">邮箱咨询</h3>
            <p class="text-gray-600">工作日 24小时内回复</p>
            <p class="text-gray-800 font-medium mt-2">contact@jiedu-appointment.com</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { onMounted, computed } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'HomePage',
  setup() {
    const store = useStore()
    
    // 获取当前登录用户信息
    const currentUser = computed(() => {
      return store.state.user && store.state.user.isLoggedIn ? store.state.user.info : null
    })
    // 页面加载时执行动画
    onMounted(() => {
      // Hero 区域标题动画 - 使用CSS类
      setTimeout(() => {
        document.querySelector('.hero-bg h1')?.classList.add('animate-fade-in')
      }, 100)
      
      setTimeout(() => {
        document.querySelector('.hero-bg p')?.classList.add('animate-fade-in')
      }, 300)
      
      setTimeout(() => {
        document.querySelectorAll('.hero-bg a').forEach(link => {
          link.classList.add('animate-fade-in')
        })
      }, 500)

      // 其他区域滚动动画
      setupScrollAnimations()
    })

    // 设置滚动动画
    const setupScrollAnimations = () => {
      const animateOnScroll = (entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('slide-in')
            observer.unobserve(entry.target)
          }
        })
      }

      const observer = new IntersectionObserver(animateOnScroll, {
        root: null,
        threshold: 0.1
      })

      // 观察各个区块
      document.querySelectorAll('section > div > div.text-center').forEach(section => {
        observer.observe(section)
      })

      // 观察网格项
      document.querySelectorAll('.grid-cols-1 > div, .grid-cols-2 > div, .grid-cols-3 > div, .grid-cols-4 > div').forEach(item => {
        observer.observe(item)
      })
    }

    return { currentUser }
  }
}
</script>

<style scoped>
  /* 自定义样式 */
  .hero-bg {
    background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%);
    position: relative;
    overflow: hidden;
  }

  .hero-bg::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: 
      radial-gradient(circle at 20% 30%, rgba(255, 255, 255, 0.1) 0%, transparent 20%),
      radial-gradient(circle at 80% 70%, rgba(255, 255, 255, 0.1) 0%, transparent 20%),
      radial-gradient(circle at 40% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 30%);
    z-index: 0;
  }

  .hero-bg > div {
    position: relative;
    z-index: 1;
  }

  /* 自定义动画效果 */
  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(30px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .slide-in {
    animation: slideIn 0.8s ease-out forwards;
  }
  
  .animate-fade-in {
    animation: fadeIn 0.8s ease-out forwards;
  }
  
  /* 确保英雄区域元素初始为不可见 */
  .hero-bg h1,
  .hero-bg p,
  .hero-bg a {
    opacity: 0;
  }

  /* 响应式调整 */
  @media (max-width: 768px) {
    .hero-bg h1 {
      font-size: 2.5rem;
    }
    
    .hero-bg p {
      font-size: 1.25rem;
    }
  }
  
  @media (max-width: 640px) {
    .grid-cols-2 {
      grid-template-columns: 1fr;
    }
    
    .hero-bg h1 {
      font-size: 1.8rem;
    }
    
    .hero-bg p {
      font-size: 1rem;
    }
  }
  </style>