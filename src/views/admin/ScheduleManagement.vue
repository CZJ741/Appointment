<template>
  <div class="schedule-management">
    <h1 class="text-2xl font-bold mb-6 text-gray-800">探访日程记录</h1>
    
    <!-- 筛选控件 -->
    <div class="mb-6">
      <div class="flex items-center">
        <label class="block text-sm font-medium text-gray-700 mr-3">探访日筛选:</label>
        <select 
          v-model="selectedVisitDay" 
          class="border border-gray-300 rounded-md px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
        >
          <option value="">全部探访日</option>
          <option v-for="dayOption in visitDayOptions" :key="dayOption.value" :value="dayOption.value">
            {{ dayOption.label }}
          </option>
        </select>
      </div>
    </div>
    
    <!-- 统计信息卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="bg-white shadow-md rounded-lg p-6">
        <div class="text-sm text-gray-500">总探访日</div>
        <div class="text-3xl font-bold text-primary mt-1">{{ totalVisitDays }}</div>
      </div>
      <div class="bg-white shadow-md rounded-lg p-6">
        <div class="text-sm text-gray-500">总批次</div>
        <div class="text-3xl font-bold text-primary mt-1">{{ totalBatches }}</div>
      </div>
      <div class="bg-white shadow-md rounded-lg p-6">
        <div class="text-sm text-gray-500">预约数量</div>
        <div class="text-3xl font-bold text-primary mt-1">{{ appointmentCount }}</div>
      </div>
    </div>
    
    <!-- 探访日程列表（多级下拉菜单） -->
    <div class="bg-white shadow-md rounded-lg overflow-hidden">
      <div v-if="isLoading" class="p-12 text-center">
        <div class="spinner mx-auto mb-4"></div>
        <p class="text-gray-500">加载中...</p>
      </div>
      <div v-else-if="filteredVisitDayBatches.length === 0" class="p-12 text-center">
        <p class="text-gray-500">暂无探访日程信息</p>
      </div>
      <div v-else>
        <!-- 第一级：探访日 -->
        <div v-for="visitDay in filteredVisitDayBatches" :key="visitDay.visitDate" class="border-b last:border-b-0">
          <!-- 探访日标题栏（可折叠） -->
          <div 
            class="bg-gradient-to-r from-blue-50 to-blue-100 p-4 flex justify-between items-center cursor-pointer hover:from-blue-100 hover:to-blue-200 transition-colors duration-200"
            @click="toggleVisitDay(visitDay.visitDate)"
          >
            <div class="flex items-center space-x-3">
              <svg 
                class="w-5 h-5 text-gray-600 transition-transform duration-200"
                :class="{ 'rotate-90': expandedVisitDays.has(visitDay.visitDate) }"
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
              <h3 class="text-lg font-semibold text-gray-800">{{ formatDate(visitDay.visitDate) }} - 探访日</h3>
            </div>
            <div class="flex items-center space-x-4">
              <div class="text-sm text-gray-600">
                {{ visitDay.batches.length }} 个批次，{{ getTotalAppointments(visitDay) }} 个预约
              </div>
            </div>
          </div>
          
          <!-- 第二级：时间段列表（可折叠） -->
          <div v-show="expandedVisitDays.has(visitDay.visitDate)" class="border-l-4 border-blue-200">
            <div v-for="batch in visitDay.batches" :key="batch.id" class="border-b last:border-b-0">
              <!-- 时间段标题栏（可折叠） -->
              <div 
                class="bg-gray-50 p-4 flex justify-between items-center cursor-pointer hover:bg-gray-100 transition-colors duration-200"
                @click="toggleBatch(batch.id)"
              >
                <div class="flex items-center space-x-3 ml-4">
                  <svg 
                    class="w-5 h-5 text-gray-600 transition-transform duration-200"
                    :class="{ 'rotate-90': expandedBatches.has(batch.id) }"
                    fill="none" 
                    viewBox="0 0 24 24" 
                    stroke="currentColor"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                  <div>
                    <div class="font-medium text-gray-800">{{ batch.timeSlot }} - 批次 {{ batch.batchNumber }}</div>
                    <div class="text-sm text-gray-500 mt-1">
                      {{ batch.appointments.length }} 个预约
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 第三级：预约记录列表 -->
              <div v-show="expandedBatches.has(batch.id)" class="ml-8">
                <div v-if="batch.appointments.length === 0" class="p-8 text-center text-gray-500">
                  暂无预约记录
                </div>
                <div v-else class="divide-y divide-gray-200">
                  <div 
                    v-for="appointment in batch.appointments" 
                    :key="appointment.id" 
                    class="p-4 hover:bg-gray-50 transition-colors duration-200"
                  >
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      <!-- 预约基本信息 -->
                      <div class="space-y-2">
                        <div class="flex items-center">
                          <span class="text-sm font-medium text-gray-500 w-24">预约号:</span>
                          <span class="text-sm text-gray-900">{{ appointment.appointment_number || appointment.id }}</span>
                        </div>
                        <div class="flex items-center">
                          <span class="text-sm font-medium text-gray-500 w-24">状态:</span>
                          <span 
                            class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                            :class="getStatusClass(appointment.status)"
                          >
                            {{ getStatusText(appointment.status) }}
                          </span>
                        </div>
                        <div class="flex items-center">
                          <span class="text-sm font-medium text-gray-500 w-24">提交时间:</span>
                          <span class="text-sm text-gray-900">{{ formatDateTime(appointment.createTime) }}</span>
                        </div>
                      </div>
                      
                      <!-- 探访人信息 -->
                      <div class="space-y-2">
                        <div class="text-sm font-medium text-gray-700 mb-2">探访人信息</div>
                        <div v-for="(visitor, index) in appointment.visitors" :key="index" class="ml-2">
                          <div class="flex items-center mb-1">
                            <span class="text-xs font-medium bg-blue-100 text-blue-800 px-2 py-0.5 rounded mr-2">
                              {{ index === 0 ? '预约人' : '随行人员' }}
                            </span>
                            <span class="text-sm text-gray-900">{{ visitor.name }}</span>
                          </div>
                          <div class="text-xs text-gray-500 ml-2">
                            {{ visitor.gender }} | {{ visitor.idCard }} | {{ visitor.phone }} | {{ visitor.relationship }}
                          </div>
                        </div>
                      </div>
                      
                      <!-- 预约备注 -->
                      <div class="space-y-2">
                        <div class="text-sm font-medium text-gray-700 mb-2">预约备注</div>
                        <div class="text-sm text-gray-600 whitespace-pre-wrap break-words bg-gray-50 p-3 rounded">
                          {{ appointment.appointmentReason || '-' }}
                        </div>
                        <div v-if="appointment.approvalNotes" class="text-xs text-gray-500 mt-1">
                          审核备注：{{ appointment.approvalNotes }}
                        </div>
                      </div>
                    </div>
                    
                    <!-- 操作按钮 -->
                    <div class="mt-4 pt-4 border-t border-gray-200 flex justify-end space-x-3">
                      <router-link 
                        :to="`/admin/appointment/${appointment.id}`"
                        class="text-primary hover:text-primary-dark text-sm font-medium transition-colors duration-200"
                      >
                        查看详情
                      </router-link>
                      <button 
                        v-if="appointment.status === 'approved'"
                        @click="handleComplete(appointment)"
                        class="text-blue-600 hover:text-blue-800 text-sm font-medium transition-colors duration-200"
                      >
                        标记完成
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
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
  name: 'ScheduleManagement',
  setup() {
    const store = useStore()
    const isLoading = ref(true)
    const allVisitDayBatches = ref([])
    
    // 控制展开/折叠状态
    const expandedVisitDays = ref(new Set())
    const expandedBatches = ref(new Set())
    
    // 探访日筛选相关
    const selectedVisitDay = ref('')
    
    // 生成已存在探访日的选项
    const visitDayOptions = computed(() => {
      const uniqueDays = new Set()
      
      allVisitDayBatches.value.forEach(visitDay => {
        if (visitDay.visitDate) {
          uniqueDays.add(visitDay.visitDate)
        }
      })
      
      const sortedDays = Array.from(uniqueDays).sort((a, b) => {
        return new Date(b) - new Date(a)
      })
      
      return sortedDays.map(day => {
        const [year, month, date] = day.split('-').map(Number)
        return {
          value: day,
          label: `${year}年${month}月${date}日`
        }
      })
    })
    
    // 加载批次信息
    const loadBatchInfo = async () => {
      try {
        isLoading.value = true
        
        const approvedAppointments = store.state.appointments.filter(app => app.status === 'approved' || app.status === 'completed')
        
        const visitDayMap = new Map()
        
        approvedAppointments.forEach(appointment => {
          if (!appointment.visitDate) return
          
          const visitDateObj = new Date(appointment.visitDate)
          if (isNaN(visitDateObj.getTime())) return
          
          const visitDate = visitDateObj.toISOString().split('T')[0]
          
          if (!visitDayMap.has(visitDate)) {
            visitDayMap.set(visitDate, {
              visitDate: appointment.visitDate,
              batches: []
            })
          }
          
          const visitDay = visitDayMap.get(visitDate)
          
          if (!appointment.visitTime) return
          
          const fullTimeSlot = appointment.visitTime
          
          const batchIndex = visitDay.batches.findIndex(batch => batch.timeSlot === fullTimeSlot)
          
          if (batchIndex === -1) {
            visitDay.batches.push({
              id: `${visitDate}-${fullTimeSlot}`,
              visitDate: appointment.visitDate,
              batchNumber: visitDay.batches.length + 1,
              timeSlot: fullTimeSlot,
              appointments: [appointment]
            })
          } else {
            const batch = visitDay.batches[batchIndex]
            batch.appointments.push(appointment)
          }
        })
        
        allVisitDayBatches.value = Array.from(visitDayMap.values()).sort((a, b) => {
          return new Date(b.visitDate) - new Date(a.visitDate)
        })
        
        const timeSlotOrder = [
          '09:00-09:30',
          '09:30-10:00',
          '10:00-10:30',
          '10:30-11:00',
          '11:00-11:30',
          '14:30-15:00',
          '15:00-15:30',
          '15:30-16:00',
          '16:00-16:30',
          '16:30-17:00'
        ]
        
        allVisitDayBatches.value.forEach(visitDay => {
          visitDay.batches.sort((a, b) => {
            const indexA = timeSlotOrder.indexOf(a.timeSlot)
            const indexB = timeSlotOrder.indexOf(b.timeSlot)
            return indexA - indexB
          })
          
          visitDay.batches.forEach((batch, index) => {
            batch.batchNumber = index + 1
            
            batch.appointments.sort((a, b) => {
              if (!a.createTime || !b.createTime) return 0
              return new Date(a.createTime) - new Date(b.createTime)
            })
          })
        })
        
      } catch (error) {
        console.error('加载批次信息失败:', error)
      } finally {
        isLoading.value = false
      }
    }
    
    // 切换探访日展开/折叠
    const toggleVisitDay = (visitDate) => {
      if (expandedVisitDays.value.has(visitDate)) {
        expandedVisitDays.value.delete(visitDate)
      } else {
        expandedVisitDays.value.add(visitDate)
      }
    }
    
    // 切换批次展开/折叠
    const toggleBatch = (batchId) => {
      if (expandedBatches.value.has(batchId)) {
        expandedBatches.value.delete(batchId)
      } else {
        expandedBatches.value.add(batchId)
      }
    }
    
    // 获取探访日的总预约数
    const getTotalAppointments = (visitDay) => {
      return visitDay.batches.reduce((total, batch) => total + batch.appointments.length, 0)
    }
    
    // 格式化日期
    const formatDate = (date) => {
      if (!date) return ''
      const d = new Date(date)
      return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
    }
    
    // 格式化日期时间
    const formatDateTime = (dateString) => {
      if (!dateString) return ''
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
        'pending': '待审核',
        'approved': '已批准',
        'rejected': '已拒绝',
        'completed': '已完成',
        'cancelled': '已取消',
        'queued': '排队中'
      }
      return statusMap[status] || status
    }
    
    // 获取状态样式
    const getStatusClass = (status) => {
      const classMap = {
        'pending': 'bg-yellow-100 text-yellow-800',
        'approved': 'bg-green-100 text-green-800',
        'rejected': 'bg-red-100 text-red-800',
        'completed': 'bg-blue-100 text-blue-800',
        'cancelled': 'bg-gray-100 text-gray-800',
        'queued': 'bg-purple-100 text-purple-800'
      }
      return classMap[status] || 'bg-gray-100 text-gray-800'
    }
    
    // 标记完成
    const handleComplete = async (appointment) => {
      const notes = prompt('请输入探访记录（可选）：')
      if (notes === null) return
      
      try {
        await store.dispatch('completeAppointment', {
          id: appointment.id,
          completionNotes: notes
        })
        alert('预约已标记为完成！')
        await loadBatchInfo()
      } catch (error) {
        alert('操作失败，请稍后重试')
        console.error('Complete error:', error)
      }
    }
    
    // 筛选后的探访日批次
    const filteredVisitDayBatches = computed(() => {
      if (!selectedVisitDay.value) {
        return allVisitDayBatches.value
      }
      
      return allVisitDayBatches.value.filter(visitDay => {
        return visitDay.visitDate === selectedVisitDay.value
      })
    })
    
    // 统计信息计算
    const totalVisitDays = computed(() => filteredVisitDayBatches.value.length)
    const totalBatches = computed(() => {
      return filteredVisitDayBatches.value.reduce((total, visitDay) => total + visitDay.batches.length, 0)
    })
    const appointmentCount = computed(() => {
      return filteredVisitDayBatches.value.reduce((total, visitDay) => {
        return total + visitDay.batches.reduce((batchTotal, batch) => {
          return batchTotal + batch.appointments.length
        }, 0)
      }, 0)
    })
    
    onMounted(async () => {
      await store.dispatch('initializeData')
      await loadBatchInfo()
    })
    
    return {
      isLoading,
      allVisitDayBatches,
      expandedVisitDays,
      expandedBatches,
      selectedVisitDay,
      visitDayOptions,
      filteredVisitDayBatches,
      totalVisitDays,
      totalBatches,
      appointmentCount,
      toggleVisitDay,
      toggleBatch,
      getTotalAppointments,
      formatDate,
      formatDateTime,
      getStatusText,
      getStatusClass,
      handleComplete
    }
  }
}
</script>

<style scoped>
.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
