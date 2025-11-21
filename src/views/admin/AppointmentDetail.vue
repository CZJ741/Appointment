<template>
  <div class="p-6">
    <!-- 返回按钮 -->
    <router-link 
      to="/admin/appointments" 
      class="inline-flex items-center px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors duration-200 mb-6"
    >
      <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
      </svg>
      返回预约列表
    </router-link>

    <!-- 页面标题 -->
    <div class="mb-8">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">预约详情</h1>
          <p class="mt-1 text-sm text-gray-500">预约号: {{ appointment?.id }}</p>
        </div>
        <div class="mt-4 md:mt-0">
          <span 
            class="px-3 py-1 rounded-full text-sm font-medium"
            :class="getStatusClass(appointment?.status)"
          >
            {{ getStatusText(appointment?.status) }}
          </span>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="bg-white rounded-xl shadow-md p-8 text-center">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary mx-auto"></div>
      <p class="mt-4 text-gray-600">加载中...</p>
    </div>

    <!-- 未找到 -->
    <div v-else-if="!appointment" class="bg-white rounded-xl shadow-md p-8 text-center">
      <svg class="h-16 w-16 text-gray-400 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <h3 class="mt-2 text-lg font-medium text-gray-900">未找到预约记录</h3>
      <p class="mt-1 text-gray-500">可能预约号不存在或已被删除</p>
      <router-link 
        to="/admin/appointments" 
        class="mt-6 inline-flex items-center px-5 py-2 bg-primary text-white rounded-md hover:bg-primary-dark transition-colors duration-200 shadow-sm"
      >
        返回预约列表
      </router-link>
    </div>

    <!-- 预约详情 -->
    <div v-else class="space-y-8">
      <!-- 基本信息 -->
      <div class="bg-white rounded-xl shadow-md overflow-hidden">
        <div class="bg-gray-50 border-b border-gray-200 px-6 py-4">
          <h2 class="text-lg font-medium text-gray-900">基本信息</h2>
        </div>
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div>
              <div class="text-sm text-gray-500">预约月份</div>
              <div class="font-medium">{{ appointment.month }}</div>
            </div>
            <div>
              <div class="text-sm text-gray-500">探访日期</div>
              <div class="font-medium">
                {{ appointment.status === 'pending' ? '待审核后确定' : formatDate(appointment.visitDate) }}
              </div>
            </div>
            <div>
              <div class="text-sm text-gray-500">探访时间</div>
              <div class="font-medium">{{ appointment?.visitTime || '待审核后确定' }}</div>
            </div>
            <div>
              <div class="text-sm text-gray-500">排队号</div>
              <div class="font-medium">{{ appointment.queueNumber }}</div>
            </div>
            <div>
              <div class="text-sm text-gray-500">提交时间</div>
              <div class="font-medium">{{ formatDateTime(appointment.createTime) }}</div>
            </div>
            <div>
              <div class="text-sm text-gray-500">预约人数</div>
              <div class="font-medium">{{ appointment.visitors.length }}人</div>
            </div>
            <div class="md:col-span-2 lg:col-span-3">
              <div class="text-sm text-gray-500">戒毒人员姓名</div>
              <div class="font-medium">{{ appointment.prisoner_name }}</div>
            </div>
            <div class="md:col-span-2 lg:col-span-3">
              <div class="text-sm text-gray-500">联系地址</div>
              <div class="font-medium">{{ appointment.visitor_address || '未提供' }}</div>
            </div>
            <div class="md:col-span-2 lg:col-span-3">
              <div class="text-sm text-gray-500">预约原因</div>
              <div class="font-medium">{{ appointment.appointment_reason || '未提供' }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 亲属信息 -->
      <div class="bg-white rounded-xl shadow-md overflow-hidden">
        <div class="bg-gray-50 border-b border-gray-200 px-6 py-4">
          <h2 class="text-lg font-medium text-gray-900">探访人信息</h2>
        </div>
        <div class="p-6">
          <div v-for="(visitor, index) in appointment.visitors" :key="visitor.id" class="mb-6 last:mb-0">
            <div class="flex items-center mb-4">
              <div class="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center text-primary font-medium mr-3">
                {{ index + 1 }}
              </div>
              <h3 class="text-base font-medium text-gray-900">探访人 {{ index + 1 }}</h3>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 pl-13">
              <div>
                <div class="text-sm text-gray-500">姓名</div>
                <div class="font-medium">{{ visitor.name }}</div>
              </div>
              <div>
                <div class="text-sm text-gray-500">性别</div>
                <div class="font-medium">{{ visitor.gender }}</div>
              </div>
              <div>
                <div class="text-sm text-gray-500">身份证号</div>
                <div class="font-medium">{{ visitor.idCard }}</div>
              </div>
              <div>
                <div class="text-sm text-gray-500">联系电话</div>
                <div class="font-medium">{{ visitor.phone }}</div>
              </div>
              <div class="md:col-span-2">
                <div class="text-sm text-gray-500">与戒毒人员关系</div>
                <div class="font-medium">{{ visitor.relationship }}</div>
              </div>
            </div>
            <div v-if="index < appointment.visitors.length - 1" class="border-b border-gray-200 mt-6"></div>
          </div>
        </div>
      </div>

      <!-- 审批信息 -->
      <div v-if="appointment.status === 'approved' && appointment.approvalInfo" class="bg-white rounded-xl shadow-md overflow-hidden">
        <div class="bg-green-50 border-b border-green-200 px-6 py-4">
          <h2 class="text-lg font-medium text-green-800">审批信息</h2>
        </div>
        <div class="p-6 bg-green-50/30">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <div class="text-sm text-gray-500">预约编号</div>
              <div class="font-medium">{{ appointment.approvalInfo.appointmentNumber }}</div>
            </div>
            <div>
              <div class="text-sm text-gray-500">接待时间</div>
              <div class="font-medium">{{ appointment.approvalInfo.receptionTime }}</div>
            </div>
            <div>
              <div class="text-sm text-gray-500">接待地点</div>
              <div class="font-medium">{{ appointment.approvalInfo.receptionLocation }}</div>
            </div>
            <div>
              <div class="text-sm text-gray-500">接待人员</div>
              <div class="font-medium">{{ appointment.approvalInfo.receptionist }}</div>
            </div>
            <div>
              <div class="text-sm text-gray-500">联系电话</div>
              <div class="font-medium">{{ appointment.approvalInfo.receptionistPhone }}</div>
            </div>
          </div>
          <div v-if="appointment.approvalInfo.notes" class="mt-6">
            <div class="text-sm text-gray-500 mb-2">备注</div>
            <div class="bg-white p-4 rounded-lg border border-green-200">
              {{ appointment.approvalInfo.notes }}
            </div>
          </div>
        </div>
      </div>

      <!-- 拒绝信息 -->
      <div v-if="appointment.status === 'rejected' && appointment.rejectionReason" class="bg-white rounded-xl shadow-md overflow-hidden">
        <div class="bg-red-50 border-b border-red-200 px-6 py-4">
          <h2 class="text-lg font-medium text-red-800">拒绝信息</h2>
        </div>
        <div class="p-6 bg-red-50/30">
          <div class="bg-white p-4 rounded-lg border border-red-200">
            {{ appointment.rejectionReason }}
          </div>
        </div>
      </div>

      <!-- 完成记录 -->
      <div v-if="appointment.status === 'completed' && appointment.completionNotes" class="bg-white rounded-xl shadow-md overflow-hidden">
        <div class="bg-blue-50 border-b border-blue-200 px-6 py-4">
          <h2 class="text-lg font-medium text-blue-800">探访记录</h2>
        </div>
        <div class="p-6 bg-blue-50/30">
          <div class="bg-white p-4 rounded-lg border border-blue-200">
            {{ appointment.completionNotes }}
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="bg-white rounded-xl shadow-md overflow-hidden">
        <div class="p-6 flex flex-wrap gap-4 justify-end">
          <!-- 待审核状态下显示审批按钮 -->
          <template v-if="appointment.status === 'pending'">
            <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">探访日期</label>
                <div class="relative flex-grow">
                  <select
                    v-model="selectedVisitDate"
                    :class="selectedVisitDate ? 
                      'w-full px-4 py-2 border-2 border-green-500 bg-green-50 rounded-md focus:ring-green-500 focus:border-green-500 transition-all duration-300 shadow-sm' : 
                      'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors duration-200'"
                  >
                    <option value="">请选择探访日期</option>
                    <option v-for="dateOption in visitDateOptions" :key="dateOption.value" :value="dateOption.value">
                      {{ dateOption.label }}
                    </option>
                  </select>
                </div>
            </div>
            <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">探访时间</label>
                <div class="relative flex-grow">
                  <select
                    v-model="selectedVisitTime"
                    :class="selectedVisitTime ? 
                      'w-full px-4 py-2 border-2 border-green-500 bg-green-50 rounded-md focus:ring-green-500 focus:border-green-500 transition-all duration-300 shadow-sm' : 
                      'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors duration-200'"
                  >
                    <option value="">请选择探访时间</option>
                    <option v-for="time in visitTimeOptions" :key="time" :value="time">
                      {{ time }}
                    </option>
                  </select>
                </div>
            </div>
            <button 
              @click="handleApprove"
              :disabled="isProcessing"
              class="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors duration-200 disabled:opacity-70 disabled:cursor-not-allowed flex items-center"
            >
              <svg v-if="!isProcessing" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              {{ isProcessing ? '处理中...' : '批准预约' }}
            </button>
            <button 
              @click="handleReject"
              :disabled="isProcessing"
              class="px-6 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors duration-200 disabled:opacity-70 disabled:cursor-not-allowed flex items-center"
            >
              <svg v-if="!isProcessing" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
              {{ isProcessing ? '处理中...' : '拒绝预约' }}
            </button>
          </template>
          
          <!-- 已批准状态下显示完成按钮 -->
          <button 
            v-else-if="appointment.status === 'approved'"
            @click="handleComplete"
            :disabled="isProcessing"
            class="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors duration-200 disabled:opacity-70 disabled:cursor-not-allowed flex items-center"
          >
            <svg v-if="!isProcessing" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {{ isProcessing ? '处理中...' : '标记完成' }}
          </button>
          
          <!-- 其他状态下的编辑按钮 -->
          <button 
            v-else
            @click="handleEdit"
            class="px-6 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors duration-200 flex items-center"
          >
            <svg class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
            </svg>
            编辑记录
          </button>
          
          <!-- 打印按钮 -->
          <button 
            @click="handlePrint"
            class="px-6 py-2 bg-gray-800 text-white rounded-md hover:bg-gray-700 transition-colors duration-200 flex items-center"
          >
            <svg class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h-10v-10h10m2 2H7a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-2m-4 6h.01M7 16h.01" />
            </svg>
            打印记录
          </button>
        </div>
      </div>
    </div>

    <!-- 拒绝预约模态框 -->
    <div v-if="showRejectModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl shadow-xl max-w-md w-full">
        <div class="bg-red-500 p-6 rounded-t-xl">
          <h2 class="text-xl font-bold text-white">拒绝预约</h2>
        </div>
        
        <div class="p-6">
          <p class="text-gray-700 mb-4">请输入拒绝原因：</p>
          <textarea
            v-model="rejectReason"
            rows="4"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-red-500 focus:border-red-500 transition-colors duration-200"
            placeholder="请详细说明拒绝原因..."
          ></textarea>
          <div v-if="rejectError" class="mt-2 text-xs text-red-600">
            {{ rejectError }}
          </div>
          
          <div class="mt-6 flex justify-end space-x-3">
            <button 
              @click="showRejectModal = false; rejectReason = ''; rejectError = ''"
              class="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors duration-200"
            >
              取消
            </button>
            <button 
              @click="confirmReject"
              :disabled="isProcessing"
              class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors duration-200 disabled:opacity-70 disabled:cursor-not-allowed"
            >
              {{ isProcessing ? '处理中...' : '确认拒绝' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'AppointmentDetail',
  setup() {
    const store = useStore()
    const route = useRoute()
    const router = useRouter()
    const loading = ref(true)
    const isProcessing = ref(false)
    const showRejectModal = ref(false)
    const rejectReason = ref('')
    const rejectError = ref('')
    const selectedVisitDate = ref('')
    const selectedVisitTime = ref('')
    const visitDateOptions = ref([])
    // 探访时间选项 - 提供几个预设时间（使用ref保持响应式）
    const visitTimeOptions = ref([
      '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
      '14:00', '14:30', '15:00', '15:30', '16:00', '16:30'
    ])

    // 获取预约ID
    const appointmentId = computed(() => route.params.id)

    // 获取预约信息
    const appointment = computed(() => {
      return store.getters.getAppointmentById(appointmentId.value)
    })
    
    // 生成未来12个月的探访日期选项
    const generateVisitDateOptions = () => {
      const options = []
      const now = new Date()
      
      // 生成从当月开始的12个月的探访日期
      for (let i = 0; i < 12; i++) {
        const targetDate = new Date(now.getFullYear(), now.getMonth() + i, 1)
        const year = targetDate.getFullYear()
        const month = targetDate.getMonth() + 1 // 1-indexed
        
        const thirdWednesday = getThirdWednesdayOfMonth(year, month)
        const visitDate = new Date(thirdWednesday)
        
        // 格式化显示标签
        const label = `${year}年${month}月探访日（${visitDate.getDate()}日 星期三）`
        
        // 只添加未来或今天的日期选项
        const today = new Date().toISOString().split('T')[0]
        if (thirdWednesday >= today) {
          options.push({
            value: thirdWednesday,
            label: label
          })
        }
      }
      
      return options
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      })
    }
    
    // 初始化探访日期选项

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

    // 批准预约 - 管理员通过日期选择器选择探访日期
    const handleApprove = async () => {
      // 检查是否选择了日期和时间
      if (!selectedVisitDate.value) {
        alert('请选择探访日期！')
        return
      }
      if (!selectedVisitTime.value) {
        alert('请选择探访时间！')
        return
      }
      
      // 验证日期有效性
      const visitDate = new Date(selectedVisitDate.value)
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      
      if (visitDate < today) {
        alert('不能选择过去的日期！')
        return
      }
      
      // 构建targetMonth参数 (YYYY-MM格式)
      let targetMonth = null
      if (selectedVisitDate.value) {
        try {
          const dateParts = selectedVisitDate.value.split('-')
          if (dateParts.length === 3) {
            const year = dateParts[0]
            const month = dateParts[1].padStart(2, '0')
            targetMonth = `${year}-${month}`
          }
        } catch (error) {
          console.error('构建targetMonth失败:', error)
          alert('日期格式错误，请重试')
          return
        }
      }
      
      if (!targetMonth) {
        alert('无法确定目标月份，请重试')
        return
      }
      
      // 检查所选月份是否已有批准的预约
      // 使用实际选择的探访日期月份进行检查，与后端逻辑保持一致
      const [targetYear, targetMonthNum] = targetMonth.split('-')
      const targetMonthAppointments = store.state.appointments.filter(app => {
        // 只检查已批准的预约
        if (app.status !== 'approved') return false
        
        // 只检查其他预约（排除当前正在处理的预约）
        if (app.id === appointment.value.id) return false
        
        // 优先使用appointment_time字段（已批准预约会有此字段）
        if (app.appointment_time) {
          try {
            const appointmentDate = new Date(app.appointment_time)
            const appYear = appointmentDate.getFullYear().toString()
            const appMonth = String(appointmentDate.getMonth() + 1).padStart(2, '0')
            return appYear === targetYear && appMonth === targetMonthNum
          } catch (error) {
            console.error('解析appointment_time失败:', error)
            return false
          }
        }
        
        return false
      })
      
      if (targetMonthAppointments.length > 0) {
        alert(`所选月份 ${targetMonth} 已有批准的预约，请选择其他月份！`)
        return
      }
      
      const confirmMessage = `确定要批准该预约吗？探访日期将安排在 ${selectedVisitDate.value}（探访日），探访时间为 ${selectedVisitTime.value}。`
      
      if (confirm(confirmMessage)) {
        try {
          isProcessing.value = true
          
          await store.dispatch('approveAppointment', {
            id: appointment.value.id,
            approvalInfo: {
              appointmentNumber: `AP${Date.now()}`,
              receptionTime: selectedVisitTime.value, // 使用选择器选择的时间
              receptionLocation: '探访室A',
              receptionist: '值班人员',
              receptionistPhone: '010-12345678'
            },
            visitDate: selectedVisitDate.value, // 使用选择器选择的日期
            targetMonth: targetMonth
          })
          
          // 成功通知
          alert('预约已成功批准并分配探访日期和时间！')
        } catch (error) {
          // 显示后端返回的具体错误信息，如果没有则显示通用错误提示
          const errorMessage = error.response?.data?.error || error.message || '操作失败，请稍后重试'
          alert(`错误：${errorMessage}`)
          console.error('Approve error:', error)
        } finally {
          isProcessing.value = false
        }
      }
    }

    // 显示拒绝模态框
    const handleReject = () => {
      showRejectModal.value = true
    }

    // 确认拒绝
    const confirmReject = async () => {
      if (!rejectReason.value.trim()) {
        rejectError.value = '请输入拒绝原因'
        return
      }
      
      try {
        isProcessing.value = true
        await store.dispatch('rejectAppointment', {
          id: appointment.value.id,
          rejectionReason: rejectReason.value
        })
        showRejectModal.value = false
        rejectReason.value = ''
        rejectError.value = ''
        alert('预约已成功拒绝！')
      } catch (error) {
        alert('操作失败，请稍后重试')
        console.error('Reject error:', error)
      } finally {
        isProcessing.value = false
      }
    }

    // 标记完成
    const handleComplete = async () => {
      const notes = prompt('请输入探访记录（可选）：')
      if (notes === null) return // 用户取消
      
      try {
        isProcessing.value = true
        await store.dispatch('completeAppointment', {
          id: appointment.value.id,
          completionNotes: notes
        })
        alert('预约已标记为完成！')
      } catch (error) {
        alert('操作失败，请稍后重试')
        console.error('Complete error:', error)
      } finally {
        isProcessing.value = false
      }
    }

    // 编辑记录
    const handleEdit = () => {
      alert('编辑功能正在开发中...')
    }

    // 打印记录
    const handlePrint = () => {
      window.print()
    }

    // 计算指定月份的第三个星期三（包含跨月处理）
  const getThirdWednesdayOfMonth = (year, month) => {
    // JS 的月份从 0 开始，函数接收1-indexed的月份，需要减1
    const first = new Date(year, month - 1, 1); 
    const dayOfWeek = first.getDay();          // 0=Sun … 3=Wed 
    const daysToWed = (3 - dayOfWeek + 7) % 7; 
    const firstWed = new Date(first); 
    firstWed.setDate(1 + daysToWed); 
    const thirdWed = new Date(firstWed); 
    thirdWed.setDate(firstWed.getDate() + 14); 
    // 跨月处理 
    if (thirdWed.getMonth() !== month - 1) { 
      thirdWed.setDate(thirdWed.getDate() - 7); 
    }
    
    // 返回完整的日期字符串 YYYY-MM-DD
    const yyyy = thirdWed.getFullYear();
    const mm = String(thirdWed.getMonth() + 1).padStart(2, '0');
    const dd = String(thirdWed.getDate()).padStart(2, '0');
    
    return `${yyyy}-${mm}-${dd}`;
  }
    
    // 加载数据
      const loadData = async () => {
        loading.value = true
        try {
          // 确保数据已初始化
          if (store.state.appointments.length === 0) {
            await store.dispatch('initializeData')
          }
          
          // 生成探访日期选项
          visitDateOptions.value = generateVisitDateOptions()
          
          // 如果预约处于待审核状态，尝试预选当前或预约月份的第三个星期三
          if (appointment.value && appointment.value.status === 'pending') {
            let targetYear, targetMonth
            
            if (appointment.value.month) {
              // 从预约月份中提取年月
              const [year, month] = appointment.value.month.split('-')
              targetYear = parseInt(year)
              targetMonth = parseInt(month)
            } else {
              // 使用当前年月
              const now = new Date()
              targetYear = now.getFullYear()
              targetMonth = now.getMonth() + 1
            }
            
            // 计算该月的第三个星期三
            const thirdWednesdayDate = getThirdWednesdayOfMonth(targetYear, targetMonth)
            
            // 尝试在选项中找到匹配的日期并预选
            const option = visitDateOptions.value.find(opt => opt.value === thirdWednesdayDate)
            if (option) {
              selectedVisitDate.value = thirdWednesdayDate
            } else if (visitDateOptions.value.length > 0) {
              // 如果没有匹配的选项，预选第一个可用选项
              selectedVisitDate.value = visitDateOptions.value[0].value
            }
            selectedVisitTime.value = ''; // 重置时间选择
          }
          // 如果已经有批准的时间，设置默认值
          else if (appointment.value && appointment.value.approvalInfo?.receptionTime) {
            selectedVisitTime.value = appointment.value.approvalInfo.receptionTime;
          }
        } catch (error) {
          console.error('加载数据失败:', error)
        } finally {
          loading.value = false
        }
      }

    onMounted(() => {
      // 检查是否已登录
      if (!store.state.isAdminLoggedIn) {
        router.push('/admin/login')
        return
      }
      
      // 加载数据
      loadData()
    })

    // 监听ID变化，重新加载数据
    watch(() => route.params.id, () => {
      loadData()
    })

    return {
      appointment,
      loading,
      isProcessing,
      showRejectModal,
      rejectReason,
      rejectError,
      selectedVisitDate,
      selectedVisitTime,
      visitDateOptions,
      visitTimeOptions,
      formatDate,
      formatDateTime,
      getStatusText,
      getStatusClass,
      handleApprove,
      handleReject,
      confirmReject,
      handleComplete,
      handleEdit,
      handlePrint
    }
  }
}
</script>

<style scoped>
/* 自定义样式 */
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

/* 按钮悬停效果 */
button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

button:active:not(:disabled) {
  transform: translateY(0);
}

/* 打印样式 */
@media print {
  .bg-white.rounded-xl {
    box-shadow: none;
    border: 1px solid #ddd;
  }
  
  button {
    display: none;
  }
  
  router-link {
    display: none;
  }
}
</style>