<template>
  <div class="max-w-5xl mx-auto">
    <div class="bg-white rounded-xl shadow-md overflow-hidden mb-8">
      <div class="bg-primary p-6">
        <h1 class="text-2xl font-bold text-white">我的预约</h1>
        <p class="text-white/80 mt-1">查看您的探访预约记录和状态</p>
      </div>

      <div class="p-6">
        <!-- 筛选器 -->
        <div class="mb-6">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div class="flex flex-wrap gap-2">
              <button 
                v-for="filter in filters" 
                :key="filter.value"
                @click="activeFilter = filter.value"
                class="px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200"
                :class="activeFilter === filter.value ? 'bg-primary text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
              >
                {{ filter.label }}
              </button>
            </div>
            <div class="relative">
              <input
                type="text"
                v-model="searchQuery"
                class="w-full md:w-64 px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors pr-10"
                placeholder="搜索预约号或姓名..."
              />
              <svg class="absolute right-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- 预约列表 -->
        <div v-if="filteredAppointments.length > 0" class="space-y-4">
          <div 
            v-for="appointment in filteredAppointments" 
            :key="appointment.id"
            class="border border-gray-200 rounded-lg overflow-hidden hover:shadow-md transition-shadow duration-300"
          >
            <div class="bg-gray-50 px-6 py-4 border-b border-gray-200 flex flex-col md:flex-row md:items-center justify-between">
              <div>
                <h3 class="text-lg font-medium text-gray-900">
                  {{ appointment.month }} 探访预约
                </h3>
                <div class="text-sm text-gray-500 mt-1">
                  <span>预约号: {{ appointment.id }}</span>
                  <span class="mx-2">|</span>
                  <span>提交时间: {{ formatDate(appointment.createTime) }}</span>
                </div>
              </div>
              <div class="mt-3 md:mt-0 flex items-center">
                <span 
                  class="px-3 py-1 rounded-full text-xs font-medium"
                  :class="getStatusClass(appointment.status)"
                >
                  {{ getStatusText(appointment.status) }}
                </span>
                <button 
                  @click="viewDetail(appointment)"
                  class="ml-4 px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors duration-200 text-sm"
                >
                  查看详情
                </button>
              </div>
            </div>
            <div class="px-6 py-4">
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <div class="text-sm text-gray-500">探访日期</div>
                  <div class="font-medium">
                    {{ appointment.status === 'approved' && appointment.visitDate ? formatDate(appointment.visitDate) : '待审核后确定' }}
                  </div>
                </div>
                <div>
                  <div class="text-sm text-gray-500">探访时间</div>
                  <div class="font-medium">
                    {{ appointment.status === 'approved' && appointment.visitTime ? appointment.visitTime : '待审核后确定' }}
                  </div>
                </div>
                <div>
                  <div class="text-sm text-gray-500">排队号</div>
                  <div class="font-medium">{{ appointment.queueNumber }}</div>
                </div>
                <!-- 戒毒人员信息 -->
                <div v-if="appointment.patientName" class="md:col-span-3">
                  <div class="text-sm text-gray-500">戒毒人员</div>
                  <div class="font-medium">{{ appointment.patientName }}</div>
                </div>
                <!-- 申请人信息 -->
                <div v-if="appointment.visitors && appointment.visitors.length > 0" class="md:col-span-3">
                  <div class="text-sm text-gray-500">申请人</div>
                  <div class="font-medium bg-blue-50 px-3 py-1.5 rounded-md inline-block">
                    {{ appointment.visitors[0].name }}
                  </div>
                </div>
                <!-- 同行亲属信息 -->
                <div v-if="appointment.visitors && appointment.visitors.length > 1" class="md:col-span-3">
                  <div class="text-sm text-gray-500">同行亲属 ({{ appointment.visitors.length - 1 }}人)</div>
                  <div class="flex flex-wrap gap-2 mt-1">
                    <div v-for="visitor in appointment.visitors.slice(1)" :key="visitor.id" class="bg-gray-100 px-3 py-1 rounded-full text-sm">
                      {{ visitor.name }}
                    </div>
                  </div>
                </div>
                <!-- 排队情况（仅对待审核状态显示） -->
                <div v-if="appointment.status === 'pending'" class="md:col-span-3 mt-2">
                  <div class="text-sm text-gray-500">当前排队情况</div>
                  <div class="font-medium text-yellow-600">
                    位置: {{ getQueuePosition(appointment.id) }}/{{ getTotalPending(appointment.month) }}
                  </div>
                </div>
                <!-- 批次信息已移除 -->
              </div>
              
              <!-- 审批信息 -->
              <div v-if="appointment.status === 'approved' && appointment.approvalInfo" class="mt-4 pt-4 border-t border-gray-200">
                <h4 class="font-medium text-gray-700 mb-2">审批信息</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <span class="text-gray-500">预约编号:</span> 
                    <span class="font-medium">{{ appointment.approvalInfo.appointmentNumber }}</span>
                  </div>
                  <div>
                    <span class="text-gray-500">接待时间:</span> 
                    <span class="font-medium">{{ appointment.approvalInfo.receptionTime }}</span>
                  </div>
                  <div>
                    <span class="text-gray-500">接待地点:</span> 
                    <span class="font-medium">{{ appointment.approvalInfo.receptionLocation }}</span>
                  </div>
                  <div>
                    <span class="text-gray-500">接待人员:</span> 
                    <span class="font-medium">{{ appointment.approvalInfo.receptionist }}</span>
                  </div>
                  <div class="md:col-span-2">
                    <span class="text-gray-500">联系电话:</span> 
                    <span class="font-medium">{{ appointment.approvalInfo.receptionistPhone }}</span>
                  </div>
                  <div v-if="appointment.approvalInfo.notes" class="md:col-span-2">
                    <span class="text-gray-500">备注:</span> 
                    <span class="font-medium text-blue-600">{{ appointment.approvalInfo.notes }}</span>
                  </div>
                </div>
              </div>
              
              <!-- 拒绝原因 -->
              <div v-if="appointment.status === 'rejected' && appointment.rejectionReason" class="mt-4 pt-4 border-t border-gray-200">
                <h4 class="font-medium text-gray-700 mb-2">拒绝原因</h4>
                <div class="text-sm text-red-600 bg-red-50 p-3 rounded-md">
                  {{ appointment.rejectionReason }}
                </div>
              </div>
              
              <!-- 完成记录 -->
              <div v-if="appointment.status === 'completed' && appointment.completionNotes" class="mt-4 pt-4 border-t border-gray-200">
                <h4 class="font-medium text-gray-700 mb-2">探访记录</h4>
                <div class="text-sm text-gray-600 bg-green-50 p-3 rounded-md">
                  {{ appointment.completionNotes }}
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 空状态 -->
        <div v-else class="text-center py-16">
          <svg class="mx-auto h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h3 class="mt-2 text-lg font-medium text-gray-900">暂无预约记录</h3>
          <p class="mt-1 text-gray-500">您还没有任何预约记录</p>
          <div class="mt-6">
            <router-link 
              to="/booking"
              class="px-6 py-2 bg-primary text-white rounded-md hover:bg-primary-dark transition-colors duration-200 shadow-sm"
            >
              立即预约
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- 预约详情模态框 -->
    <div v-if="selectedAppointment" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="bg-primary p-6 rounded-t-xl">
          <div class="flex justify-between items-center">
            <h2 class="text-xl font-bold text-white">预约详情</h2>
            <button 
              @click="closeDetail"
              class="text-white hover:text-gray-200 transition-colors"
            >
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        
        <div class="p-6">
          <div class="space-y-6">
            <!-- 基本信息 -->
            <div>
              <h3 class="text-lg font-medium text-gray-900 mb-3">基本信息</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <span class="text-gray-500">预约月份:</span> 
                  <span class="font-medium">{{ selectedAppointment.month }}</span>
                </div>
                <div>
                  <span class="text-gray-500">预约状态:</span> 
                  <span 
                    class="px-2 py-1 rounded-full text-xs font-medium"
                    :class="getStatusClass(selectedAppointment.status)"
                  >
                    {{ getStatusText(selectedAppointment.status) }}
                  </span>
                </div>
                <div>
                  <span class="text-gray-500">探访日期:</span> 
                  <span class="font-medium">
                    {{ selectedAppointment.status === 'approved' && selectedAppointment.visitDate ? 
                       formatDate(selectedAppointment.visitDate) : '待审核后确定' }}
                  </span>
                </div>
                <div>
                  <span class="text-gray-500">探访时间:</span> 
                  <span class="font-medium">
                    {{ selectedAppointment.status === 'approved' && selectedAppointment.visitTime ? 
                       selectedAppointment.visitTime : '待审核后确定' }}
                  </span>
                </div>
                <div>
                  <span class="text-gray-500">排队号:</span> 
                  <span class="font-medium">{{ selectedAppointment.queueNumber }}</span>
                </div>
                <div>
                  <span class="text-gray-500">批次:</span> 
                  <span class="font-medium">第 {{ selectedAppointment.batchNumber }} 批次</span>
                </div>
                <!-- 排队情况 -->
                <div v-if="selectedAppointment.status === 'pending'">
                  <span class="text-gray-500">当前排队位置:</span> 
                  <span class="font-medium text-yellow-600">{{ getQueuePosition(selectedAppointment.id) }}</span>
                </div>
                <div v-if="selectedAppointment.status === 'pending'">
                  <span class="text-gray-500">队列总人数:</span> 
                  <span class="font-medium">{{ getTotalPending(selectedAppointment.month) }}</span>
                </div>
                <div>
                  <span class="text-gray-500">提交时间:</span> 
                  <span class="font-medium">{{ formatDateTime(selectedAppointment.createTime) }}</span>
                </div>
              </div>
            </div>
            
            <!-- 戒毒人员信息 -->
            <div v-if="selectedAppointment.patientName" class="mb-6">
              <h3 class="text-lg font-medium text-gray-900 mb-3">戒毒人员信息</h3>
              <div class="p-3 border border-gray-200 rounded-lg text-sm">
                <div>
                  <span class="text-gray-500">姓名:</span> 
                  <span class="font-medium">{{ selectedAppointment.patientName }}</span>
                </div>
              </div>
            </div>
            
            <!-- 申请人信息 -->
            <div class="mb-6">
              <h3 class="text-lg font-medium text-gray-900 mb-3">申请人信息</h3>
              <div v-if="selectedAppointment.visitors && selectedAppointment.visitors.length > 0" class="p-3 border border-gray-200 rounded-lg">
                <h4 class="font-medium mb-2">{{ selectedAppointment.visitors[0].name }}</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
                  <div>
                    <span class="text-gray-500">性别:</span> 
                    <span class="font-medium">{{ selectedAppointment.visitors[0].gender }}</span>
                  </div>
                  <div>
                    <span class="text-gray-500">身份证号:</span> 
                    <span class="font-medium">{{ maskIdCard(selectedAppointment.visitors[0].idCard) }}</span>
                  </div>
                  <div>
                    <span class="text-gray-500">联系电话:</span> 
                    <span class="font-medium">{{ maskPhone(selectedAppointment.visitors[0].phone) }}</span>
                  </div>
                  <div>
                    <span class="text-gray-500">与被探访人关系:</span> 
                    <span class="font-medium">{{ selectedAppointment.visitors[0].relationship }}</span>
                  </div>
                  <div v-if="selectedAppointment.applicantAddress" class="md:col-span-2">
                    <span class="text-gray-500">地址:</span> 
                    <span class="font-medium">{{ selectedAppointment.applicantAddress }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 其他亲属信息 -->
            <div v-if="selectedAppointment.visitors && selectedAppointment.visitors.length > 1">
              <h3 class="text-lg font-medium text-gray-900 mb-3">同行亲属信息</h3>
              <div v-for="(visitor, index) in selectedAppointment.visitors.slice(1)" :key="visitor.id" class="mb-4 last:mb-0 p-3 border border-gray-200 rounded-lg">
                <h4 class="font-medium mb-2">亲属 {{ index }}: {{ visitor.name }}</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
                  <div>
                    <span class="text-gray-500">性别:</span> 
                    <span class="font-medium">{{ visitor.gender }}</span>
                  </div>
                  <div>
                    <span class="text-gray-500">身份证号:</span> 
                    <span class="font-medium">{{ maskIdCard(visitor.idCard) }}</span>
                  </div>
                  <div>
                    <span class="text-gray-500">联系电话:</span> 
                    <span class="font-medium">{{ maskPhone(visitor.phone) }}</span>
                  </div>
                  <div class="md:col-span-2">
                    <span class="text-gray-500">与被探访人关系:</span> 
                    <span class="font-medium">{{ visitor.relationship }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 审批信息 -->
            <div v-if="selectedAppointment.status === 'approved' && selectedAppointment.approvalInfo">
              <h3 class="text-lg font-medium text-gray-900 mb-3">审批信息</h3>
              <div class="bg-green-50 p-4 rounded-lg">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <span class="text-gray-500">预约编号:</span> 
                    <span class="font-medium">{{ selectedAppointment.approvalInfo.appointmentNumber }}</span>
                  </div>
                  <div>
                    <span class="text-gray-500">接待时间:</span> 
                    <span class="font-medium">{{ selectedAppointment.approvalInfo.receptionTime }}</span>
                  </div>
                  <div>
                    <span class="text-gray-500">接待地点:</span> 
                    <span class="font-medium">{{ selectedAppointment.approvalInfo.receptionLocation }}</span>
                  </div>
                  <div>
                    <span class="text-gray-500">接待人员:</span> 
                    <span class="font-medium">{{ selectedAppointment.approvalInfo.receptionist }}</span>
                  </div>
                  <div>
                    <span class="text-gray-500">联系电话:</span> 
                    <span class="font-medium">{{ selectedAppointment.approvalInfo.receptionistPhone }}</span>
                  </div>
                </div>
                <div v-if="selectedAppointment.approvalInfo.notes" class="mt-4 text-sm">
                  <span class="text-gray-500 block mb-1">备注:</span> 
                  <div class="font-medium text-blue-600 bg-white p-2 rounded">
                    {{ selectedAppointment.approvalInfo.notes }}
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 拒绝原因 -->
            <div v-if="selectedAppointment.status === 'rejected' && selectedAppointment.rejectionReason">
              <h3 class="text-lg font-medium text-gray-900 mb-3">拒绝原因</h3>
              <div class="bg-red-50 p-4 rounded-lg text-sm">
                <div class="text-red-600">
                  {{ selectedAppointment.rejectionReason }}
                </div>
              </div>
            </div>
            
            <!-- 完成记录 -->
            <div v-if="selectedAppointment.status === 'completed' && selectedAppointment.completionNotes">
              <h3 class="text-lg font-medium text-gray-900 mb-3">探访记录</h3>
              <div class="bg-blue-50 p-4 rounded-lg text-sm">
                <div class="text-gray-700">
                  {{ selectedAppointment.completionNotes }}
                </div>
              </div>
            </div>
          </div>
          
          <div class="mt-6 text-right">
            <button 
              @click="closeDetail"
              class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors duration-200"
            >
              关闭
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'AppointmentsPage',
  setup() {
    const store = useStore()
    const activeFilter = ref('all')
    const searchQuery = ref('')
    const selectedAppointment = ref(null)

    const filters = [
      { label: '全部', value: 'all' },
      { label: '待审核', value: 'pending' },
      { label: '已批准', value: 'approved' },
      { label: '已拒绝', value: 'rejected' },
      { label: '已完成', value: 'completed' }
    ]

    // 获取用户的预约
    const filteredAppointments = computed(() => {
      // 使用userAppointments getter获取当前用户的预约
      let result = store.getters.userAppointments

      // 状态过滤
      if (activeFilter.value !== 'all') {
        result = result.filter(appointment => appointment.status === activeFilter.value)
      }

      // 搜索过滤
      if (searchQuery.value.trim()) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(appointment => {
          // 搜索预约号
          if (appointment.id.toLowerCase().includes(query)) return true
          
          // 搜索亲属姓名
          return appointment.visitors.some(visitor => 
            visitor.name.toLowerCase().includes(query)
          )
        })
      }

      // 按创建时间倒序排列
      return result.sort((a, b) => new Date(b.createTime) - new Date(a.createTime))
    })

    // 获取预约的排队位置
    const getQueuePosition = (appointmentId) => {
      return store.getters.appointmentQueuePosition(appointmentId)
    }
    
    // 获取特定月份的待审核预约总数
    const getTotalPending = (month) => {
      return store.state.appointments.filter(appt => 
        appt.month === month && appt.status === 'pending'
      ).length
    }

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
        year: 'numeric',
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

    // 身份证号脱敏
    const maskIdCard = (idCard) => {
      if (!idCard || idCard.length < 10) return idCard
      return idCard.substring(0, 6) + '********' + idCard.substring(idCard.length - 4)
    }

    // 手机号脱敏
    const maskPhone = (phone) => {
      if (!phone || phone.length < 11) return phone
      return phone.substring(0, 3) + '****' + phone.substring(phone.length - 4)
    }

    // 查看详情
    const viewDetail = (appointment) => {
      selectedAppointment.value = appointment
    }

    // 关闭详情
    const closeDetail = () => {
      selectedAppointment.value = null
    }

    // 监听点击模态框外部关闭
    onMounted(async () => {
      // 从后端获取最新的预约数据
      await store.dispatch('initializeData')
      
      const handleClickOutside = (event) => {
        if (selectedAppointment.value && 
            event.target.classList.contains('fixed') && 
            event.target.classList.contains('bg-black')) {
          closeDetail()
        }
      }
      
      document.addEventListener('click', handleClickOutside)
      
      return () => {
        document.removeEventListener('click', handleClickOutside)
      }
    })

    return {
      activeFilter,
      searchQuery,
      filters,
      filteredAppointments,
      selectedAppointment,
      formatDate,
      formatDateTime,
      getStatusText,
      getStatusClass,
      maskIdCard,
      maskPhone,
      viewDetail,
      closeDetail,
      getQueuePosition,
      getTotalPending
    }
  }
}
</script>

<style scoped>
/* 自定义样式 */
/* 模态框动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.scale-enter-active,
.scale-leave-active {
  transition: transform 0.3s ease;
}

.scale-enter-from {
  transform: scale(0.9);
}

.scale-leave-to {
  transform: scale(0.9);
}

/* 滚动条样式 */
.max-h-\[90vh\]::-webkit-scrollbar {
  width: 6px;
}

.max-h-\[90vh\]::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.max-h-\[90vh\]::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.max-h-\[90vh\]::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>