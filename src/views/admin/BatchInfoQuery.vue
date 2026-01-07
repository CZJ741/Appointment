<template>
  <div class="batch-info-query">
    <h1 class="text-2xl font-bold mb-6 text-gray-800">批次信息查询</h1>
    
    <!-- 筛选控件 -->
    <div class="mb-6">
      <div class="flex items-center">
        <label class="block text-sm font-medium text-gray-700 mr-3">年月筛选:</label>
        <select 
          v-model="selectedMonth" 
          class="border border-gray-300 rounded-md px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
        >
          <option value="">全部年月</option>
          <option v-for="monthOption in monthOptions" :key="monthOption.value" :value="monthOption.value">
            {{ monthOption.label }}
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
    
    <!-- 探访日批次列表 -->
    <div class="bg-white shadow-md rounded-lg overflow-hidden">
      <div v-if="isLoading" class="p-12 text-center">
        <div class="spinner mx-auto mb-4"></div>
        <p class="text-gray-500">加载中...</p>
      </div>
      <div v-else-if="allVisitDayBatches.length === 0" class="p-12 text-center">
        <p class="text-gray-500">暂无批次信息</p>
      </div>
      <div v-else>
        <!-- 探访日分组 -->
        <div v-for="visitDay in paginatedVisitDayBatches" :key="visitDay.visitDate" class="border-b last:border-b-0">
          <div class="bg-gray-50 p-4 flex justify-between items-center">
        <h3 class="text-lg font-semibold text-gray-800">{{ formatDate(visitDay.visitDate) }} - 探访日</h3>
        <div class="flex items-center space-x-4">
          <div class="text-sm text-gray-500">
            {{ visitDay.batches.length }} 个批次
          </div>
        </div>
      </div>
          
          <!-- 批次列表 -->
          <div class="p-4">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">批次号</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">时间段</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">已用配额</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">可用配额</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">总配额</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="batch in visitDay.batches" :key="batch.id" class="hover:bg-gray-50 transition-colors duration-200">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ batch.batchNumber }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ batch.timeSlot }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ batch.usedQuota }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ batch.availableQuota }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ batch.totalQuota }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button 
                      @click="viewBatchDetails(batch)" 
                      class="text-primary hover:text-primary-dark transition-colors duration-200"
                    >
                      查看详情
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        
        <!-- 分页 -->
        <div class="p-4 bg-gray-50 flex justify-between items-center">
          <div class="text-sm text-gray-500">
            显示第 {{ (currentPage - 1) * pageSize + 1 }} 到第 {{ Math.min(currentPage * pageSize, allVisitDayBatches.length) }} 条，共 {{ allVisitDayBatches.length }} 条
          </div>
          <div class="flex space-x-2">
            <button 
              @click="currentPage = 1" 
              :disabled="currentPage === 1"
              class="px-3 py-1 border rounded text-sm hover:bg-gray-100 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              首页
            </button>
            <button 
              @click="currentPage--" 
              :disabled="currentPage === 1"
              class="px-3 py-1 border rounded text-sm hover:bg-gray-100 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              上一页
            </button>
            <button 
              @click="currentPage++" 
              :disabled="currentPage >= totalPages"
              class="px-3 py-1 border rounded text-sm hover:bg-gray-100 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              下一页
            </button>
            <button 
              @click="currentPage = totalPages" 
              :disabled="currentPage >= totalPages"
              class="px-3 py-1 border rounded text-sm hover:bg-gray-100 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              末页
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 批次详情弹窗 -->
    <div v-if="showBatchDetails" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center" @click="showBatchDetails = false">
      <div class="bg-white rounded-lg shadow-xl max-w-[93.6rem] w-full max-h-[80vh] overflow-y-auto" @click.stop>
        <div class="p-6 border-b">
          <h2 class="text-xl font-bold text-gray-800">批次详情</h2>
          <button 
            @click="showBatchDetails = false" 
            class="absolute top-4 right-4 text-gray-500 hover:text-gray-700"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div v-if="selectedBatch" class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <div class="text-sm text-gray-500">探访日期</div>
              <div class="font-medium mt-1">{{ formatDate(selectedBatch.visitDate) }}</div>
            </div>
            <div>
              <div class="text-sm text-gray-500">批次号</div>
              <div class="font-medium mt-1">{{ selectedBatch.batchNumber }}</div>
            </div>
            <div>
              <div class="text-sm text-gray-500">时间段</div>
              <div class="font-medium mt-1">{{ selectedBatch.timeSlot }}</div>
            </div>
            <div>
              <div class="text-sm text-gray-500">总配额</div>
              <div class="font-medium mt-1">{{ selectedBatch.totalQuota }}</div>
            </div>
            <div>
              <div class="text-sm text-gray-500">已用配额</div>
              <div class="font-medium mt-1">{{ selectedBatch.usedQuota }}</div>
            </div>
            <div>
              <div class="text-sm text-gray-500">可用配额</div>
              <div class="font-medium mt-1">{{ selectedBatch.availableQuota }}</div>
            </div>
          </div>
          
          <!-- 该批次的预约列表 -->
          <div class="mt-8">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">该批次预约列表</h3>
            <div v-if="selectedBatch.appointments.length === 0" class="text-center py-8 text-gray-500">
              暂无预约
            </div>
            <div v-else>
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">预约号</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">预约人数</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">探访人</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">性别</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">身份证号</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">联系电话</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">与戒毒人员关系</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">戒毒人员</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">联系地址</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">预约原因</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">提交时间</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="appointment in selectedBatch.appointments" :key="appointment.id" class="hover:bg-gray-50 transition-colors duration-200">
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ appointment.appointment_number || appointment.id }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ appointment.visitors?.length || 1 }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ appointment.visitors[0]?.name || appointment.visitor_name || '-' }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ appointment.visitors[0]?.gender || '-' }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ appointment.visitors[0]?.idCard || appointment.visitor_id_card || '-' }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ appointment.visitors[0]?.phone || appointment.visitor_phone || '-' }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ appointment.visitors[0]?.relationship || '-' }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ appointment.prisonerName || appointment.prisoner_name || '-' }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ appointment.visitor_address || '-' }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ appointment.appointment_reason || appointment.reason || '-' }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ appointment.createTime ? formatDateTime(appointment.createTime) : '-' }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span 
                        class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                        :class="getStatusClass(appointment.status)"
                      >
                        {{ getStatusText(appointment.status) }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'BatchInfoQuery',
  setup() {
    const store = useStore()
    const isLoading = ref(true)
    const allVisitDayBatches = ref([])
    const showBatchDetails = ref(false)
    const selectedBatch = ref(null)
    
    // 月份筛选相关
    const selectedMonth = ref('') // 选中的月份，格式为 'YYYY-MM'
    
    // 生成已存在探访日的年月选项
    const monthOptions = computed(() => {
      // 从所有探访日中提取唯一的年月
      const uniqueMonths = new Set()
      
      allVisitDayBatches.value.forEach(visitDay => {
        if (visitDay.visitDate) {
          // 将YYYY-MM-DD转换为YYYY-MM格式
          const yearMonth = visitDay.visitDate.substring(0, 7)
          uniqueMonths.add(yearMonth)
        }
      })
      
      // 转换为数组并排序（最新的年月在前）
      const sortedMonths = Array.from(uniqueMonths).sort((a, b) => {
        return new Date(b + '-01') - new Date(a + '-01')
      })
      
      // 生成选项列表
      return sortedMonths.map(yearMonth => {
        const [year, month] = yearMonth.split('-')
        return {
          value: yearMonth,
          label: `${year}年${parseInt(month)}月`
        }
      })
    })
    
    // 分页相关
    const currentPage = ref(1)
    const pageSize = ref(5) // 每页显示5个探访日
    
    // 加载批次信息
    const loadBatchInfo = async () => {
      try {
        isLoading.value = true
        console.log('开始加载批次信息...')
        console.log('管理员登录状态:', store.state.isAdminLoggedIn)
        console.log('store中所有预约数量:', store.state.appointments.length)
        
        // 从store获取已批准的预约
        const approvedAppointments = store.state.appointments.filter(app => app.status === 'approved' || app.status === 'completed')
        console.log('已批准/已完成的预约数量:', approvedAppointments.length)
        console.log('已批准/已完成的预约:', approvedAppointments)
        
        // 按探访日分组
        const visitDayMap = new Map()
        
        approvedAppointments.forEach(appointment => {
          console.log('处理预约:', appointment.id, '状态:', appointment.status, '探访日期:', appointment.visitDate, '探访时间:', appointment.visitTime)
          
          if (!appointment.visitDate) {
            console.log('跳过没有探访日期的预约:', appointment.id)
            return
          }
          
          // 检查探访日期是否有效
          const visitDateObj = new Date(appointment.visitDate)
          if (isNaN(visitDateObj.getTime())) {
            console.log('跳过无效探访日期的预约:', appointment.id, '日期:', appointment.visitDate)
            return
          }
          
          const visitDate = visitDateObj.toISOString().split('T')[0]
          
          if (!visitDayMap.has(visitDate)) {
            visitDayMap.set(visitDate, {
              visitDate: appointment.visitDate,
              batches: []
            })
          }
          
          const visitDay = visitDayMap.get(visitDate)
          
          // 检查探访时间是否有效
          if (!appointment.visitTime) {
            console.log('跳过没有探访时间的预约:', appointment.id)
            return
          }
          
          // 直接使用visitTime作为时间段（它已经是完整的时间段格式，如"09:00-09:30"）
          const fullTimeSlot = appointment.visitTime
          
          // 按时间段分组批次
          const batchIndex = visitDay.batches.findIndex(batch => batch.timeSlot === fullTimeSlot)
          
          if (batchIndex === -1) {
            // 新批次
            visitDay.batches.push({
              id: `${visitDate}-${fullTimeSlot}`,
              visitDate: appointment.visitDate,
              batchNumber: visitDay.batches.length + 1,
              timeSlot: fullTimeSlot,
              usedQuota: 1,
              availableQuota: 2 - 1, // 总配额改为2
              totalQuota: 2,
              appointments: [appointment]
            })
          } else {
            // 已有批次，更新配额和预约列表
            const batch = visitDay.batches[batchIndex]
            batch.usedQuota += 1
            // 确保availableQuota不会小于0
            batch.availableQuota = Math.max(0, batch.availableQuota - 1)
            batch.appointments.push(appointment)
          }
        })
        
        // 转换为数组并排序
        allVisitDayBatches.value = Array.from(visitDayMap.values()).sort((a, b) => {
          return new Date(b.visitDate) - new Date(a.visitDate)
        })
        
        // 定义时间段的顺序，用于正确排序
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
        
        // 按时间段顺序对每个探访日的批次排序
        allVisitDayBatches.value.forEach(visitDay => {
          visitDay.batches.sort((a, b) => {
            const indexA = timeSlotOrder.indexOf(a.timeSlot)
            const indexB = timeSlotOrder.indexOf(b.timeSlot)
            return indexA - indexB
          })
          
          // 重新计算批次号
          visitDay.batches.forEach((batch, index) => {
            batch.batchNumber = index + 1
            
            // 按预约提交时间排序预约列表
            batch.appointments.sort((a, b) => {
              // 确保createTime存在且为有效日期
              if (!a.createTime || !b.createTime) return 0
              return new Date(a.createTime) - new Date(b.createTime)
            })
          })
        })
        
        // 重置当前页到第一页
        currentPage.value = 1
        
        console.log('最终生成的探访日批次:', allVisitDayBatches.value)
        
      } catch (error) {
        console.error('加载批次信息失败:', error)
      } finally {
        isLoading.value = false
        console.log('批次信息加载完成，isLoading:', isLoading.value)
      }
    }
    
    // 查看批次详情
    const viewBatchDetails = (batch) => {
      selectedBatch.value = batch
      showBatchDetails.value = true
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
    
    // 筛选后的探访日批次
    const filteredVisitDayBatches = computed(() => {
      if (!selectedMonth.value) {
        return allVisitDayBatches.value
      }
      
      // 解析选中的月份 (YYYY-MM)
      const [year, month] = selectedMonth.value.split('-').map(Number)
      
      return allVisitDayBatches.value.filter(visitDay => {
        const visitDate = new Date(visitDay.visitDate)
        return visitDate.getFullYear() === year && visitDate.getMonth() + 1 === month
      })
    })
    
    // 分页相关计算属性
    const paginatedVisitDayBatches = computed(() => {
      const startIndex = (currentPage.value - 1) * pageSize.value
      const endIndex = startIndex + pageSize.value
      return filteredVisitDayBatches.value.slice(startIndex, endIndex)
    })
    
    const totalPages = computed(() => {
      return Math.ceil(filteredVisitDayBatches.value.length / pageSize.value)
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
    
    // 监听选中月份变化，重置页码
    watch(selectedMonth, () => {
      currentPage.value = 1
    })
    
    // 打印探访日信息
    const printVisitDay = (visitDay) => {
      console.log('准备打印探访日:', visitDay.visitDate)
      console.log('探访日批次:', visitDay.batches)
      
      // 创建打印内容
      const printContent = document.createElement('table')
      printContent.className = 'print-pure-table'
      
      // 创建探访日标题行
      const titleRow = document.createElement('tr')
      const titleCell = document.createElement('th')
      titleCell.setAttribute('colspan', '6')
      titleCell.textContent = `探访日：${formatDate(visitDay.visitDate)}`
      titleRow.appendChild(titleCell)
      printContent.appendChild(titleRow)
      
      // 按时间段顺序处理批次
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
      
      // 为每个时间段创建表格部分
      timeSlotOrder.forEach(timeSlot => {
        const batch = visitDay.batches.find(b => b.timeSlot === timeSlot)
        
        if (batch && batch.appointments.length > 0) {
          // 创建时间段标题行
          const timeSlotRow = document.createElement('tr')
          const timeSlotCell = document.createElement('td')
          timeSlotCell.setAttribute('colspan', '6')
          timeSlotCell.textContent = `时间段：${timeSlot}`
          timeSlotRow.appendChild(timeSlotCell)
          printContent.appendChild(timeSlotRow)
          
          // 创建表头行
          const headerRow = document.createElement('tr')
          const headers = ['预约号', '探访人', '联系电话', '戒毒人员', '预约原因', '状态']
          headers.forEach(header => {
            const th = document.createElement('th')
            th.textContent = header
            headerRow.appendChild(th)
          })
          printContent.appendChild(headerRow)
          
          // 添加预约数据行
          batch.appointments.forEach(appointment => {
            const dataRow = document.createElement('tr')
            
            const idCell = document.createElement('td')
            idCell.textContent = appointment.appointment_number || appointment.id
            dataRow.appendChild(idCell)
            
            const visitorCell = document.createElement('td')
            visitorCell.textContent = appointment.visitors[0]?.name || '-'  
            dataRow.appendChild(visitorCell)
            
            const phoneCell = document.createElement('td')
            phoneCell.textContent = appointment.visitors[0]?.phone || appointment.visitor_phone || '-'  
            dataRow.appendChild(phoneCell)
            
            const prisonerCell = document.createElement('td')
            prisonerCell.textContent = appointment.prisonerName || '-'
            dataRow.appendChild(prisonerCell)
            
            const reasonCell = document.createElement('td')
            reasonCell.textContent = appointment.appointment_reason || appointment.reason || '-'
            dataRow.appendChild(reasonCell)
            
            const statusCell = document.createElement('td')
            statusCell.textContent = getStatusText(appointment.status)
            dataRow.appendChild(statusCell)
            
            printContent.appendChild(dataRow)
          })
        }
      })
      
      // 将打印内容添加到页面
      document.body.appendChild(printContent)
      
      // 触发打印
      window.print()
      
      // 打印完成后移除打印内容
      setTimeout(() => {
        document.body.removeChild(printContent)
      }, 100)
    }
    
    // 初始化
    onMounted(() => {
      // 加载所有预约数据
      store.dispatch('initializeData').then(() => {
        loadBatchInfo()
      })
    })
    
    return {
      isLoading,
      allVisitDayBatches,
      paginatedVisitDayBatches,
      currentPage,
      pageSize,
      totalPages,
      showBatchDetails,
      selectedBatch,
      totalVisitDays,
      totalBatches,
      appointmentCount,
      loadBatchInfo,
      viewBatchDetails,
      formatDate,
      formatDateTime,
      getStatusText,
      getStatusClass,
      selectedMonth,
      monthOptions
    }
  }
}
</script>

<style scoped>
/* 自定义样式 */
</style>
