<template>
  <div class="p-6">
    <!-- 页面标题 -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900">预约管理</h1>
      <p class="mt-1 text-sm text-gray-500">查看和处理所有预约请求</p>
    </div>

    <!-- 筛选和搜索 -->
    <div class="bg-white rounded-xl shadow-md p-6 mb-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- 状态筛选 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">状态筛选</label>
          <select 
            v-model="filters.status" 
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors duration-200"
          >
            <option value="all">全部状态</option>
            <option value="pending">待审核</option>
            <option value="approved">已批准</option>
            <option value="rejected">已拒绝</option>
            <option value="completed">已完成</option>
          </select>
        </div>
        
        <!-- 月份筛选 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">月份筛选</label>
          <select 
            v-model="filters.month" 
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors duration-200"
          >
            <option value="all">全部月份</option>
            <option value="1月">1月</option>
            <option value="2月">2月</option>
            <option value="3月">3月</option>
            <option value="4月">4月</option>
            <option value="5月">5月</option>
            <option value="6月">6月</option>
            <option value="7月">7月</option>
            <option value="8月">8月</option>
            <option value="9月">9月</option>
            <option value="10月">10月</option>
            <option value="11月">11月</option>
            <option value="12月">12月</option>
          </select>
        </div>
        
        <!-- 搜索框 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">搜索</label>
          <div class="relative">
            <input
              v-model="filters.search"
              type="text"
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors duration-200 pr-10"
              placeholder="搜索预约号或探访人姓名"
            />
            <svg class="absolute right-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>
      </div>
      
      <!-- 日期范围筛选 -->
      <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">开始日期</label>
          <input
            v-model="filters.startDate"
            type="date"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors duration-200"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">结束日期</label>
          <input
            v-model="filters.endDate"
            type="date"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors duration-200"
          />
        </div>
      </div>
      
      <!-- 操作按钮 -->
      <div class="mt-6 flex flex-wrap gap-4">
        <button 
          @click="applyFilters" 
          class="px-5 py-2 bg-primary text-white rounded-md hover:bg-primary-dark transition-colors duration-200 shadow-sm"
        >
          应用筛选
        </button>
        <button 
          @click="resetFilters" 
          class="px-5 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors duration-200"
        >
          重置筛选
        </button>
        <button 
          @click="exportData" 
          class="px-5 py-2 bg-gray-800 text-white rounded-md hover:bg-gray-700 transition-colors duration-200 ml-auto"
        >
          导出数据
          <svg class="inline h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
        </button>
      </div>
    </div>

    <!-- 预约列表 -->
    <div class="bg-white rounded-xl shadow-md overflow-hidden mb-8">
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
                探访时间
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                预约人数
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
            <tr v-for="appointment in filteredAppointments" :key="appointment.id" class="hover:bg-gray-50 transition-colors duration-200">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ appointment.id }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ appointment.visitors[0]?.name || '-' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ appointment.status === 'approved' && appointment.visitDate ? 
                   formatDate(appointment.visitDate) : '待审核后确定' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ appointment.visitTime }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ appointment.visitors.length }}人
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
                  @click="handleDelete(appointment)"
                  class="text-red-600 hover:text-red-800 mr-3 transition-colors duration-200"
                >
                  删除
                </button>
                
                <!-- 待审核状态下显示审批按钮 -->
                <template v-if="appointment.status === 'pending'">
                  <button 
                    @click="handleApprove(appointment)"
                    class="text-green-600 hover:text-green-800 mr-3 transition-colors duration-200"
                  >
                    批准
                  </button>
                  <button 
                    @click="handleReject(appointment)"
                    class="text-red-600 hover:text-red-800 transition-colors duration-200"
                  >
                    拒绝
                  </button>
                </template>
                
                <!-- 已批准状态下显示完成按钮 -->
                <button 
                  v-else-if="appointment.status === 'approved'"
                  @click="handleComplete(appointment)"
                  class="text-blue-600 hover:text-blue-800 transition-colors duration-200"
                >
                  标记完成
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- 空状态 -->
      <div v-if="filteredAppointments.length === 0" class="text-center py-16">
        <svg class="mx-auto h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 class="mt-2 text-lg font-medium text-gray-900">暂无符合条件的预约记录</h3>
        <p class="mt-1 text-gray-500">请尝试调整筛选条件</p>
        <button 
          @click="resetFilters" 
          class="mt-6 px-6 py-2 bg-primary text-white rounded-md hover:bg-primary-dark transition-colors duration-200 shadow-sm"
        >
          重置筛选
        </button>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="filteredAppointments.length > 0" class="bg-white rounded-xl shadow-md p-6">
      <div class="flex items-center justify-between">
        <div class="text-sm text-gray-500">
          显示 {{ startIndex }} 到 {{ endIndex }} 条，共 {{ filteredAppointments.length }} 条
        </div>
        <div class="flex space-x-2">
          <button 
            @click="currentPage = 1" 
            :disabled="currentPage === 1"
            class="px-3 py-1 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            首页
          </button>
          <button 
            @click="currentPage--" 
            :disabled="currentPage === 1"
            class="px-3 py-1 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            上一页
          </button>
          
          <!-- 页码按钮 -->
          <button 
            v-for="page in visiblePages" 
            :key="page"
            @click="currentPage = page"
            class="px-3 py-1 border border-gray-300 rounded-md transition-colors"
            :class="currentPage === page ? 'bg-primary text-white' : 'text-gray-700 hover:bg-gray-50'"
          >
            {{ page }}
          </button>
          
          <button 
            @click="currentPage++" 
            :disabled="currentPage === totalPages"
            class="px-3 py-1 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            下一页
          </button>
          <button 
            @click="currentPage = totalPages" 
            :disabled="currentPage === totalPages"
            class="px-3 py-1 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            末页
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
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'AppointmentsList',
  setup() {
    const store = useStore()
    const router = useRouter()
    const currentPage = ref(1)
    const itemsPerPage = 10
    const showRejectModal = ref(false)
    const selectedAppointment = ref(null)
    const rejectReason = ref('')
    const rejectError = ref('')
    const isProcessing = ref(false)

    // 筛选条件
    const filters = ref({
      status: 'all',
      month: 'all',
      search: '',
      startDate: '',
      endDate: ''
    })

    // 获取所有预约
    const appointments = computed(() => {
      return store.state.appointments
    })

    // 过滤预约
    const filteredAppointments = computed(() => {
      let result = [...appointments.value]

      // 状态过滤
      if (filters.value.status !== 'all') {
        result = result.filter(a => a.status === filters.value.status)
      }

      // 月份过滤 - 支持待审核和已批准预约的月份筛选
      if (filters.value.month !== 'all') {
        result = result.filter(a => {
          // 对于已批准的预约，使用visitDate的月份
          if (a.status === 'approved' && a.visitDate) {
            const visitMonth = new Date(a.visitDate).getMonth() + 1
            return visitMonth.toString().padStart(2, '0') === filters.value.month
          }
          // 对于待审核的预约，使用原有的month字段（创建月份）
          return a.month === filters.value.month
        })
      }

      // 搜索过滤
      if (filters.value.search.trim()) {
        const query = filters.value.search.toLowerCase()
        result = result.filter(a => 
          a.id.toLowerCase().includes(query) || 
          a.visitors.some(v => v.name.toLowerCase().includes(query))
        )
      }

      // 开始日期过滤 - 只对有日期的预约进行过滤
      if (filters.value.startDate) {
        const start = new Date(filters.value.startDate)
        result = result.filter(a => !a.visitDate || new Date(a.visitDate) >= start)
      }

      // 结束日期过滤 - 只对有日期的预约进行过滤
      if (filters.value.endDate) {
        const end = new Date(filters.value.endDate)
        end.setHours(23, 59, 59, 999)
        result = result.filter(a => !a.visitDate || new Date(a.visitDate) <= end)
      }

      // 按创建时间倒序排列
      return result.sort((a, b) => new Date(b.createTime) - new Date(a.createTime))
    })

    // 分页相关计算
    const totalPages = computed(() => {
      return Math.ceil(filteredAppointments.value.length / itemsPerPage)
    })

    const startIndex = computed(() => {
      return filteredAppointments.value.length === 0 ? 0 : (currentPage.value - 1) * itemsPerPage + 1
    })

    const endIndex = computed(() => {
      return Math.min(currentPage.value * itemsPerPage, filteredAppointments.value.length)
    })

    // 可见页码
    const visiblePages = computed(() => {
      const total = totalPages.value
      const current = currentPage.value
      const pages = []
      
      if (total <= 5) {
        for (let i = 1; i <= total; i++) {
          pages.push(i)
        }
      } else {
        if (current <= 3) {
          for (let i = 1; i <= 5; i++) {
            pages.push(i)
          }
        } else if (current >= total - 2) {
          for (let i = total - 4; i <= total; i++) {
            pages.push(i)
          }
        } else {
          for (let i = current - 2; i <= current + 2; i++) {
            pages.push(i)
          }
        }
      }
      
      return pages
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

    // 应用筛选
    const applyFilters = () => {
      currentPage.value = 1
    }

    // 重置筛选
    const resetFilters = () => {
      filters.value = {
        status: 'all',
        month: 'all',
        search: '',
        startDate: '',
        endDate: ''
      }
      currentPage.value = 1
    }


    
    // 批准预约 - 支持选择具体日期
    const handleApprove = async (appointment) => {
      try {
        isProcessing.value = true
        
        // 允许管理员选择具体的探访日期
        let selectedVisitDate = prompt('请输入探访日期 (格式: YYYY-MM-DD):');
        
        // 验证日期格式
        while (selectedVisitDate) {
          // 简单的日期格式验证
          const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
          if (!dateRegex.test(selectedVisitDate)) {
            selectedVisitDate = prompt('日期格式不正确，请输入探访日期 (格式: YYYY-MM-DD):');
            continue;
          }
          
          // 验证日期有效性
          const dateObj = new Date(selectedVisitDate);
          if (isNaN(dateObj.getTime())) {
            selectedVisitDate = prompt('无效的日期，请重新输入 (格式: YYYY-MM-DD):');
            continue;
          }
          
          // 检查是否为过去的日期
          const today = new Date();
          today.setHours(0, 0, 0, 0);
          if (dateObj < today) {
            selectedVisitDate = prompt('不能选择过去的日期，请重新输入 (格式: YYYY-MM-DD):');
            continue;
          }
          
          break;
        }
        
        // 如果用户取消日期输入
        if (!selectedVisitDate) return;
        
        // 根据选择的日期确定月份
        const dateObj = new Date(selectedVisitDate);
        const selectedMonth = `${dateObj.getFullYear()}-${String(dateObj.getMonth() + 1).padStart(2, '0')}`;
        
        // 检查该月份是否已有批准的预约
        const hasMonthApproved = store.state.appointments.some(a => 
          a.id !== appointment.id && // 排除当前预约
          (a.month === selectedMonth || 
           (a.visitDate && new Date(a.visitDate).getFullYear() === dateObj.getFullYear() && 
            new Date(a.visitDate).getMonth() === dateObj.getMonth())) &&
          a.status === 'approved'
        );
        
        if (hasMonthApproved) {
          alert(`月份 ${selectedMonth} 已有批准的预约批次，一个月只能接待一个预约！`);
          return;
        }
        
        // 确认批准
        if (confirm(`确定要批准预约号 ${appointment.id} 吗？\n\n探访日期：${selectedVisitDate}`)) {
          // 调用store action批准预约
          await store.dispatch('approveAppointment', {
            id: appointment.id,
            approvalInfo: {
              appointmentNumber: `AP${Date.now()}`,
              receptionTime: `${appointment.visitTime}`,
              receptionLocation: '探访室A',
              receptionist: '值班人员',
              receptionistPhone: '010-12345678'
            },
            visitDate: selectedVisitDate, // 传入具体的探访日期
            targetMonth: selectedMonth // 传递目标月份
          })
          
          alert(`预约已成功批准！\n探访日期：${visitDateDisplay}`);
        }
      } catch (error) {
        // 显示具体的错误信息
        alert(`操作失败：${error.message || '请稍后重试'}`);
        console.error('Approve error:', error);
      } finally {
        isProcessing.value = false
      }
    }

    // 显示拒绝模态框
    const handleReject = (appointment) => {
      selectedAppointment.value = appointment
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
          id: selectedAppointment.value.id,
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
    const handleComplete = async (appointment) => {
      const notes = prompt('请输入探访记录（可选）：')
      if (notes === null) return // 用户取消
      
      try {
        isProcessing.value = true
        await store.dispatch('completeAppointment', {
          id: appointment.id,
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

    // 导出数据
    const exportData = () => {
      alert('导出功能正在开发中...')
    }

    // 删除预约
    const handleDelete = async (appointment) => {
      if (confirm(`确定要删除预约号 ${appointment.id} 吗？此操作不可恢复！`)) {
        try {
          isProcessing.value = true
          await store.dispatch('deleteAppointment', appointment.id)
          alert('预约已成功删除！')
        } catch (error) {
          alert('删除失败，请稍后重试')
          console.error('Delete error:', error)
        } finally {
          isProcessing.value = false
        }
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
    })

    return {
      filters,
      currentPage,
      filteredAppointments,
      totalPages,
      startIndex,
      endIndex,
      visiblePages,
      showRejectModal,
      rejectReason,
      rejectError,
      isProcessing,
      formatDate,
      formatDateTime,
      getStatusText,
      getStatusClass,
      applyFilters,
      resetFilters,
      handleApprove,
      handleReject,
      confirmReject,
      handleComplete,
      exportData,
      handleDelete
    }
  }
}
</script>

<style scoped>
/* 自定义样式 */
/* 模态框动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* 表格行悬停效果增强 */
tbody tr:hover {
  background-color: rgba(249, 250, 251, 0.8);
}

/* 按钮悬停效果 */
button:hover:not(:disabled) {
  transform: translateY(-1px);
}

/* 响应式调整 */
@media (max-width: 640px) {
  .grid-cols-1\/md\:grid-cols-3 {
    grid-template-columns: 1fr;
  }
  
  .grid-cols-1\/md\:grid-cols-2 {
    grid-template-columns: 1fr;
  }
}
</style>