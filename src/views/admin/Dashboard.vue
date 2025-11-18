<template>
  <div class="p-6">
    <!-- 页面标题 -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900">管理控制台</h1>
      <p class="mt-1 text-sm text-gray-500">欢迎回来，{{ adminName }}！这是今天的系统概览。</p>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <!-- 总预约数 -->
      <div class="bg-white rounded-xl shadow-md p-6 border-l-4 border-primary hover:shadow-lg transition-shadow duration-300">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-500">总预约数</p>
            <h3 class="text-2xl font-bold text-gray-900 mt-1">{{ stats.totalAppointments }}</h3>
            <p class="text-xs text-green-600 flex items-center mt-2">
              <svg class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
              </svg>
              <span>本月比上月增长 {{ stats.growthRate }}%</span>
            </p>
          </div>
          <div class="p-3 bg-primary/10 rounded-lg">
            <svg class="h-6 w-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
            </svg>
          </div>
        </div>
      </div>

      <!-- 待审核 -->
      <div class="bg-white rounded-xl shadow-md p-6 border-l-4 border-yellow-500 hover:shadow-lg transition-shadow duration-300">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-500">待审核预约</p>
            <h3 class="text-2xl font-bold text-gray-900 mt-1">{{ stats.pendingAppointments }}</h3>
            <p class="text-xs text-gray-500 flex items-center mt-2">
              <span>{{ stats.pendingPercentage }}% 的总预约</span>
            </p>
          </div>
          <div class="p-3 bg-yellow-100 rounded-lg">
            <svg class="h-6 w-6 text-yellow-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
      </div>

      <!-- 已批准 -->
      <div class="bg-white rounded-xl shadow-md p-6 border-l-4 border-green-500 hover:shadow-lg transition-shadow duration-300">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-500">已批准预约</p>
            <h3 class="text-2xl font-bold text-gray-900 mt-1">{{ stats.approvedAppointments }}</h3>
            <p class="text-xs text-gray-500 flex items-center mt-2">
              <span>{{ stats.approvedPercentage }}% 的总预约</span>
            </p>
          </div>
          <div class="p-3 bg-green-100 rounded-lg">
            <svg class="h-6 w-6 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
        </div>
      </div>

      <!-- 已拒绝 -->
      <div class="bg-white rounded-xl shadow-md p-6 border-l-4 border-red-500 hover:shadow-lg transition-shadow duration-300">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-500">已拒绝预约</p>
            <h3 class="text-2xl font-bold text-gray-900 mt-1">{{ stats.rejectedAppointments }}</h3>
            <p class="text-xs text-gray-500 flex items-center mt-2">
              <span>{{ stats.rejectedPercentage }}% 的总预约</span>
            </p>
          </div>
          <div class="p-3 bg-red-100 rounded-lg">
            <svg class="h-6 w-6 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- 快捷操作 -->
    <div class="bg-white rounded-xl shadow-md p-6 mb-8">
      <h2 class="text-lg font-medium text-gray-900 mb-4">快捷操作</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <router-link 
          to="/admin/appointments" 
          class="block p-4 border border-gray-200 rounded-lg hover:bg-primary/5 hover:border-primary transition-colors duration-200 text-center"
        >
          <div class="inline-flex items-center justify-center p-3 bg-primary/10 rounded-full mb-3">
            <svg class="h-6 w-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
            </svg>
          </div>
          <h3 class="text-base font-medium text-gray-900">管理预约</h3>
          <p class="mt-1 text-sm text-gray-500">查看和处理所有预约请求</p>
        </router-link>
        
        <div class="block p-4 border border-gray-200 rounded-lg hover:bg-primary/5 hover:border-primary transition-colors duration-200 text-center">
          <div class="inline-flex items-center justify-center p-3 bg-primary/10 rounded-full mb-3">
            <svg class="h-6 w-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <h3 class="text-base font-medium text-gray-900">用户管理</h3>
          <p class="mt-1 text-sm text-gray-500">管理系统用户和权限</p>
        </div>
        
        <div class="block p-4 border border-gray-200 rounded-lg hover:bg-primary/5 hover:border-primary transition-colors duration-200 text-center">
          <div class="inline-flex items-center justify-center p-3 bg-primary/10 rounded-full mb-3">
            <svg class="h-6 w-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h3 class="text-base font-medium text-gray-900">系统设置</h3>
          <p class="mt-1 text-sm text-gray-500">配置系统参数和规则</p>
        </div>
        
        <div class="block p-4 border border-gray-200 rounded-lg hover:bg-primary/5 hover:border-primary transition-colors duration-200 text-center">
          <div class="inline-flex items-center justify-center p-3 bg-primary/10 rounded-full mb-3">
            <svg class="h-6 w-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 class="text-base font-medium text-gray-900">导出报告</h3>
          <p class="mt-1 text-sm text-gray-500">生成和下载系统报告</p>
        </div>
      </div>
    </div>

    <!-- 最近预约 -->
    <div class="bg-white rounded-xl shadow-md p-6 mb-8">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-lg font-medium text-gray-900">最近预约</h2>
        <router-link 
          to="/admin/appointments" 
          class="text-primary hover:text-primary-dark text-sm font-medium transition-colors duration-200"
        >
          查看全部
          <svg class="inline h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
          </svg>
        </router-link>
      </div>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                预约号
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                探访人
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                探访日期
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                状态
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                提交时间
              </th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                操作
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="appointment in recentAppointments" :key="appointment.id" class="hover:bg-gray-50 transition-colors duration-200">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ appointment.id }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ appointment.visitors[0]?.name }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(appointment.visitDate) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span 
                  class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                  :class="getStatusClass(appointment.status)"
                >
                  {{ getStatusText(appointment.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDateTime(appointment.createTime) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <router-link 
                  :to="`/admin/appointment/${appointment.id}`"
                  class="text-primary hover:text-primary-dark mr-3 transition-colors duration-200"
                >
                  查看详情
                </router-link>
                <button 
                  v-if="appointment.status === 'pending'"
                  @click="handleQuickApprove(appointment)"
                  class="text-green-600 hover:text-green-900 transition-colors duration-200"
                >
                  快速批准
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div v-if="recentAppointments.length === 0" class="text-center py-8 text-gray-500">
        暂无最近预约记录
      </div>
    </div>

    <!-- 月度统计图表 -->
    <div class="bg-white rounded-xl shadow-md p-6">
      <h2 class="text-lg font-medium text-gray-900 mb-6">月度预约统计</h2>
      <div class="h-64">
        <canvas ref="chartCanvas"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'Dashboard',
  setup() {
    const store = useStore()
    const router = useRouter()
    const chartCanvas = ref(null)
    const chartInstance = ref(null)

    // 计算统计数据
    const stats = computed(() => {
      const appointments = store.state.appointments
      const total = appointments.length
      const pending = appointments.filter(a => a.status === 'pending').length
      const approved = appointments.filter(a => a.status === 'approved').length
      const rejected = appointments.filter(a => a.status === 'rejected').length
      
      // 模拟增长数据
      const growthRate = 12.5
      
      return {
        totalAppointments: total,
        pendingAppointments: pending,
        approvedAppointments: approved,
        rejectedAppointments: rejected,
        growthRate: growthRate,
        pendingPercentage: total > 0 ? Math.round((pending / total) * 100) : 0,
        approvedPercentage: total > 0 ? Math.round((approved / total) * 100) : 0,
        rejectedPercentage: total > 0 ? Math.round((rejected / total) * 100) : 0
      }
    })

    // 最近预约
    const recentAppointments = computed(() => {
      return store.state.appointments
        .sort((a, b) => new Date(b.createTime) - new Date(a.createTime))
        .slice(0, 5)
    })

    // 管理员名称
    const adminName = computed(() => {
      return store.state.adminInfo?.username || '管理员'
    })

    // 格式化日期
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      })
    }

    // 格式化日期时间
    const formatDateTime = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN', {
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    // 获取状态文本
    const getStatusText = (status) => {
      const statusMap = {
        pending: '待审核',
        approved: '已批准',
        rejected: '已拒绝',
        completed: '已完成'
      }
      return statusMap[status] || status
    }

    // 获取状态样式类
    const getStatusClass = (status) => {
      const classMap = {
        pending: 'bg-yellow-100 text-yellow-800',
        approved: 'bg-green-100 text-green-800',
        rejected: 'bg-red-100 text-red-800',
        completed: 'bg-blue-100 text-blue-800'
      }
      return classMap[status] || 'bg-gray-100 text-gray-800'
    }

    // 快速批准
    const handleQuickApprove = async (appointment) => {
      // 显示确认对话框
      if (confirm(`确定要批准预约号 ${appointment.id} 吗？请在详情页面中设置具体的探访日期。`)) {
        try {
          await store.dispatch('approveAppointment', {
            id: appointment.id,
            approvalInfo: {
              notes: '快速批准'
            },
            visitDate: null,
            targetMonth: appointment.month || ''
          })
          // 显示成功消息
          alert('预约已成功批准，请在详情页面中设置探访日期')
        } catch (error) {
          alert('操作失败，请稍后重试')
          console.error('Quick approve error:', error)
        }
      }
    }

    // 初始化图表
    const initChart = () => {
      // 动态导入Chart.js及所需组件
      import('chart.js/auto').then((ChartJS) => {
        // 使用导入的Chart对象
        const Chart = ChartJS.default || window.Chart
        
        if (chartCanvas.value) {
          // 销毁旧图表
          if (chartInstance.value) {
            chartInstance.value.destroy()
          }

          const ctx = chartCanvas.value.getContext('2d')
          
          // 模拟过去6个月的数据
          const months = ['1月', '2月', '3月', '4月', '5月', '6月']
          const pendingData = [15, 22, 18, 25, 30, 28]
          const approvedData = [45, 55, 60, 70, 75, 82]
          const rejectedData = [10, 8, 12, 15, 10, 12]

          chartInstance.value = new Chart(ctx, {
            type: 'bar',
            data: {
              labels: months,
              datasets: [
                {
                  label: '待审核',
                  data: pendingData,
                  backgroundColor: '#FCD34D',
                  borderColor: '#F59E0B',
                  borderWidth: 1
                },
                {
                  label: '已批准',
                  data: approvedData,
                  backgroundColor: '#34D399',
                  borderColor: '#10B981',
                  borderWidth: 1
                },
                {
                  label: '已拒绝',
                  data: rejectedData,
                  backgroundColor: '#FCA5A5',
                  borderColor: '#EF4444',
                  borderWidth: 1
                }
              ]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              scales: {
                x: {
                  stacked: true,
                  grid: {
                    display: false
                  }
                },
                y: {
                  stacked: true,
                  beginAtZero: true
                }
              },
              plugins: {
                legend: {
                  position: 'top',
                },
                tooltip: {
                  mode: 'index',
                  intersect: false
                }
              }
            }
          })
        }
      })
    }

    // 监听窗口大小变化，重绘图表
    const handleResize = () => {
      if (chartInstance.value) {
        chartInstance.value.resize()
      }
    }

    onMounted(async () => {
      // 检查是否已登录
      if (!store.state.isAdminLoggedIn) {
        router.push('/admin/login')
        return
      }

      // 从后端获取最新的预约数据
      await store.dispatch('initializeData')
      
      // 初始化图表
      initChart()
      
      // 添加窗口大小变化监听
      window.addEventListener('resize', handleResize)
    })

    // 组件卸载时清理
    const cleanup = () => {
      window.removeEventListener('resize', handleResize)
      if (chartInstance.value) {
        chartInstance.value.destroy()
      }
    }

    return {
      chartCanvas,
      stats,
      recentAppointments,
      adminName,
      formatDate,
      formatDateTime,
      getStatusText,
      getStatusClass,
      handleQuickApprove
    }
  }
}
</script>

<style scoped>
/* 自定义动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 卡片进入动画 */
.bg-white.rounded-xl {
  animation: fadeIn 0.5s ease-out;
}

/* 统计卡片悬停效果 */
.bg-white.rounded-xl:hover {
  transform: translateY(-2px);
}

/* 表格行悬停效果增强 */
tbody tr:hover {
  background-color: rgba(249, 250, 251, 0.8);
}

/* 响应式调整 */
@media (max-width: 640px) {
  .grid-cols-1\/md\:grid-cols-4 {
    grid-template-columns: 1fr 1fr;
  }
}
</style>