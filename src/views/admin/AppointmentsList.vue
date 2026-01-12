<template>
  <div class="p-6 relative h-screen overflow-hidden flex flex-col">
    <!-- 页面标题 -->
    <div class="mb-4 flex-shrink-0">
      <h1 class="text-2xl font-bold text-gray-900">预约管理</h1>
      <p class="mt-1 text-sm text-gray-500">查看和处理所有预约请求（勾选部分探访预约，为其分配时间段，后点击审核开始逐个审核）</p>
    </div>

    <!-- 探访日选择区域 - 显著位置 -->
    <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl shadow-md p-5 mb-6 border-2 border-blue-200">
      <div class="flex items-center justify-between">
        <div class="flex items-center flex-1">
          <div class="flex-shrink-0 mr-4">
            <svg class="w-8 h-8 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <div class="flex-1">
            <label class="block text-base font-semibold text-gray-900 mb-2">
              <span class="text-red-500">*</span> 请先选择探访日
            </label>
            <select 
              v-model="filters.visitDate" 
              class="w-full max-w-md px-4 py-2.5 border-2 border-blue-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 text-base font-medium"
            >
              <option value="">-- 请选择探访日 --</option>
              <option value="2026-01-14">2026年1月14日</option>
              <option value="2026-02-10">2026年2月10日</option>
              <option value="2026-03-18">2026年3月18日</option>
              <option value="2026-04-15">2026年4月15日</option>
              <option value="2026-05-13">2026年5月13日</option>
              <option value="2026-06-17">2026年6月17日</option>
              <option value="2026-07-15">2026年7月15日</option>
              <option value="2026-08-12">2026年8月12日</option>
              <option value="2026-09-16">2026年9月16日</option>
              <option value="2026-10-14">2026年10月14日</option>
              <option value="2026-11-18">2026年11月18日</option>
              <option value="2026-12-16">2026年12月16日</option>
            </select>
          </div>
        </div>
        <div v-if="!filters.visitDate" class="flex-shrink-0 ml-6">
          <div class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 rounded-r-lg max-w-xs">
            <div class="flex items-center">
              <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
              <span class="text-sm font-medium">必须先选择探访日才能进行时间段分配和审核</span>
            </div>
          </div>
        </div>
        <div v-else class="flex-shrink-0 ml-6">
          <div class="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 rounded-r-lg">
            <div class="flex items-center">
              <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
              <span class="text-sm font-medium">已选择：{{ formatVisitDate(filters.visitDate) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="flex gap-6 flex-1 overflow-hidden">
      <!-- 左侧内容 - 可滚动 -->
      <div class="flex-1 overflow-y-auto pr-2">
        <!-- 筛选和搜索 -->
        <div class="bg-white rounded-xl shadow-md p-6 mb-6">
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
            
            <!-- 排序方式 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">排序方式</label>
              <select 
                v-model="filters.sortBy" 
                class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors duration-200"
              >
                <option value="asc">按提交时间正序</option>
                <option value="desc">按提交时间逆序</option>
              </select>
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
              class="px-5 py-2 bg-gray-800 text-white rounded-md hover:bg-gray-700 transition-colors duration-200"
            >
              导出数据
              <svg class="inline h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
            </button>
          </div>
        </div>

        <!-- 预约列表 -->
        <div class="bg-white rounded-xl shadow-md overflow-hidden mb-6">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                <input 
                  type="checkbox" 
                  @change="toggleSelectAll" 
                  :checked="isAllSelected" 
                  class="rounded border-gray-300 text-primary focus:ring-primary"
                  style="width: 26px; height: 26px; cursor: pointer;"
                />
              </th>
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
                预约人数
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                预约备注
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
            <tr v-for="appointment in paginatedAppointments" :key="appointment.id" class="hover:bg-gray-50 transition-colors duration-200">
              <td class="px-6 py-4 whitespace-nowrap">
                <input 
                  type="checkbox" 
                  v-model="selectedAppointments" 
                  :value="appointment.id" 
                  :disabled="appointment.status !== 'pending'"
                  class="rounded border-gray-300 text-primary focus:ring-primary"
                  style="width: 26px; height: 26px; cursor: pointer;"
                />
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ appointment.appointment_number || appointment.id }}
              </td>
              <td class="px-6 py-4 text-sm text-gray-500">
                {{ appointment.visitors.map(v => v.name).filter(Boolean).join('、') || '-' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ appointment.visitDate ? formatDate(appointment.visitDate) : '-' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ appointment.visitors.length }}人
              </td>
              <td class="px-6 py-4 text-sm text-gray-500 max-w-xs">
                <div class="whitespace-pre-wrap break-words">{{ appointment.appointmentReason || '-' }}</div>
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
                
                <!-- 已批准状态下显示完成按钮 -->
                <button 
                  v-if="appointment.status === 'approved'"
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
        <!-- 未选择探访日时的提示 -->
        <div v-if="!filters.visitDate">
          <svg class="mx-auto h-16 w-16 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <h3 class="mt-2 text-lg font-medium text-gray-900">请先选择探访日</h3>
          <p class="mt-1 text-gray-500">选择探访日后查看该日期的预约记录</p>
        </div>
        <!-- 选择探访日但没有预约时的提示 -->
        <div v-else>
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
      </div>

      <!-- 右侧固定时间段选择 -->
      <div class="w-72 flex-shrink-0">
        <div class="bg-white rounded-xl shadow-md p-6 sticky top-0">
          <div class="mb-4 p-3 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-100">
            <div class="text-xs text-blue-600 font-medium mb-1">当前探访日</div>
            <div class="text-lg font-bold text-blue-900">
              {{ formatVisitDate(filters.visitDate) }}
            </div>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-4">选择探访时间段</h3>
          
          <!-- 未选择探访日时的提示 -->
          <div v-if="!filters.visitDate" class="text-center py-8">
            <svg class="w-16 h-16 mx-auto text-gray-300 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <p class="text-sm text-gray-500 mb-2">请先选择探访日</p>
            <p class="text-xs text-gray-400">选择探访日后才能分配时间段</p>
          </div>
          
          <!-- 选择探访日后显示时间段 -->
          <div v-else class="space-y-3">
            <div class="text-sm font-medium text-gray-600 mb-2">上午</div>
            <button
              v-for="slot in timeSlots.slice(0, 4)"
              :key="slot"
              @click="selectedTimeSlot = selectedTimeSlot === slot ? null : slot"
              class="w-full px-4 py-3 border rounded-md transition-colors duration-200 text-left"
              :class="selectedTimeSlot === slot ? 'bg-primary text-white border-primary' : 'border-gray-300 text-gray-700 hover:border-primary'"
            >
              <div class="flex justify-between items-center">
                <span>{{ slot }}</span>
                <span class="text-xs font-medium" :class="selectedTimeSlot === slot ? 'text-white/80' : getTimeSlotCountClass(slot)">
                  {{ timeSlotCounts[slot] }}/20
                </span>
              </div>
            </button>
            <div class="text-sm font-medium text-gray-600 mb-2 mt-4">下午</div>
            <button
              v-for="slot in timeSlots.slice(4)"
              :key="slot"
              @click="selectedTimeSlot = selectedTimeSlot === slot ? null : slot"
              class="w-full px-4 py-3 border rounded-md transition-colors duration-200 text-left"
              :class="selectedTimeSlot === slot ? 'bg-primary text-white border-primary' : 'border-gray-300 text-gray-700 hover:border-primary'"
            >
              <div class="flex justify-between items-center">
                <span>{{ slot }}</span>
                <span class="text-xs font-medium" :class="selectedTimeSlot === slot ? 'text-white/80' : getTimeSlotCountClass(slot)">
                  {{ timeSlotCounts[slot] }}/20
                </span>
              </div>
            </button>
          </div>
          <div class="mt-4 p-3 bg-blue-50 rounded-md">
            <p class="text-xs text-blue-700">
              <span class="font-semibold">提示：</span>选择时间段后，审核通过的预约将自动分配到此时间段
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- 固定在右下角的开始审核按钮 -->
    <button
      @click="startBatchReview"
      :disabled="selectedAppointments.length === 0 || !filters.visitDate"
      class="fixed bottom-8 right-8 px-6 py-3 bg-green-500 text-white rounded-lg shadow-lg hover:bg-green-600 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 z-40"
    >
      <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      开始审核 ({{ selectedAppointments.length }})
    </button>

    <!-- 拒绝预约模态框 -->
    <div v-if="showRejectModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl shadow-xl max-w-md w-full">
        <div class="bg-red-500 p-6 rounded-t-xl">
          <h2 class="text-xl font-bold text-white">拒绝预约</h2>
        </div>
        
        <div class="p-6 overflow-y-auto flex-1">
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
    
    <!-- 批量审核模态框 -->
    <div v-if="showBatchReviewModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        <div class="bg-primary p-6 rounded-t-xl flex justify-between items-center">
          <h2 class="text-xl font-bold text-white">批量审核预约</h2>
          <button 
            @click="closeBatchReviewModal"
            class="text-white hover:bg-white/20 rounded-full p-1 transition-colors duration-200"
            title="关闭"
          >
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="p-6 overflow-y-auto flex-1">
          <div v-if="selectedAppointments.length > 0 && currentReviewIndex < selectedAppointments.length">
            <div class="mb-6">
              <h3 class="text-lg font-semibold text-gray-900 mb-2">
                审核进度：{{ currentReviewIndex + 1 }}/{{ selectedAppointments.length }}
              </h3>
              <div class="w-full bg-gray-200 rounded-full h-8 flex overflow-hidden cursor-pointer" @click="handleProgressBarClick">
                <div
                  v-for="(appointmentId, index) in selectedAppointments"
                  :key="appointmentId"
                  class="h-8 transition-all duration-200 hover:brightness-90"
                  :class="getProgressBarItemClass(appointmentId, index)"
                  :style="{ width: (100 / selectedAppointments.length) + '%' }"
                  :title="`预约 ${index + 1}: ${getReviewStatusText(appointmentId)}`"
                ></div>
              </div>
              <div class="flex justify-between mt-2 text-xs text-gray-500">
                <span>点击进度条可跳转到对应预约</span>
                <span>
                  <span class="inline-block w-3 h-3 bg-green-500 rounded mr-1"></span>已批准
                  <span class="inline-block w-3 h-3 bg-red-500 rounded ml-2 mr-1"></span>已拒绝
                  <span class="inline-block w-3 h-3 bg-gray-300 rounded ml-2 mr-1"></span>待审核
                </span>
              </div>
            </div>
            
            <div v-if="getCurrentReviewAppointment" class="mb-6">
              <div class="space-y-4">
                <div class="bg-gray-50 rounded-lg p-4">
                  <h4 class="font-medium text-gray-900 mb-3">基本信息</h4>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                    <div>
                      <span class="text-gray-500">预约号：</span>
                      <span class="font-medium">{{ getCurrentReviewAppointment.appointment_number || getCurrentReviewAppointment.id }}</span>
                    </div>
                    <div>
                      <span class="text-gray-500">探访日期：</span>
                      <span class="font-medium">{{ getCurrentReviewAppointment.visitDate ? formatDate(getCurrentReviewAppointment.visitDate) : '待确定' }}</span>
                    </div>
                    <div>
                      <span class="text-gray-500">探访时间：</span>
                      <span class="font-medium">{{ getCurrentReviewAppointment.time_slot || '待确定' }}</span>
                    </div>
                    <div>
                      <span class="text-gray-500">提交时间：</span>
                      <span class="font-medium">{{ formatDateTime(getCurrentReviewAppointment.createTime) }}</span>
                    </div>
                    <div>
                      <span class="text-gray-500">预约人数：</span>
                      <span class="font-medium">{{ getCurrentReviewAppointment.visitors.length }}人</span>
                    </div>
                    <div>
                      <span class="text-gray-500">已选时间段：</span>
                      <span class="font-medium text-primary">{{ selectedTimeSlot }}</span>
                    </div>
                    <div class="md:col-span-2">
                      <span class="text-gray-500">戒毒人员姓名：</span>
                      <span class="font-medium">{{ getCurrentReviewAppointment.prisoner_name }}</span>
                    </div>
                    <div class="md:col-span-2">
                      <span class="text-gray-500">联系地址：</span>
                      <span class="font-medium">{{ getCurrentReviewAppointment.visitor_address || '未提供' }}</span>
                    </div>
                    <div class="md:col-span-2">
                      <span class="text-gray-500">预约备注：</span>
                      <span class="font-medium">{{ getCurrentReviewAppointment.appointment_reason || '未提供' }}</span>
                    </div>
                  </div>
                </div>

                <div class="bg-gray-50 rounded-lg p-4">
                  <h4 class="font-medium text-gray-900 mb-3">探访人信息</h4>
                  <div v-for="(visitor, index) in getCurrentReviewAppointment.visitors" :key="visitor.id" class="mb-4 last:mb-0">
                    <div class="flex items-center mb-2">
                      <div class="h-6 w-6 rounded-full bg-primary/10 flex items-center justify-center text-primary text-xs font-medium mr-2">
                        {{ index + 1 }}
                      </div>
                      <span class="text-sm font-medium text-gray-900">
                        探访人 {{ index + 1 }}
                        <span v-if="index === 0" class="ml-2 px-2 py-0.5 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">预约人</span>
                        <span v-else class="ml-2 px-2 py-0.5 text-xs font-medium bg-gray-100 text-gray-600 rounded-full">随行人员</span>
                      </span>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm pl-8">
                      <div>
                        <span class="text-gray-500">姓名：</span>
                        <span class="font-medium">{{ visitor.name }}</span>
                      </div>
                      <div>
                        <span class="text-gray-500">性别：</span>
                        <span class="font-medium">{{ visitor.gender }}</span>
                      </div>
                      <div>
                        <span class="text-gray-500">身份证号：</span>
                        <span class="font-medium">{{ visitor.idCard }}</span>
                      </div>
                      <div>
                        <span class="text-gray-500">联系电话：</span>
                        <span class="font-medium">{{ visitor.phone }}</span>
                      </div>
                      <div class="md:col-span-2">
                        <span class="text-gray-500">与戒毒人员关系：</span>
                        <span class="font-medium">{{ visitor.relationship }}</span>
                      </div>
                    </div>
                    <div v-if="index < getCurrentReviewAppointment.visitors.length - 1" class="border-b border-gray-200 mt-3"></div>
                  </div>
                </div>
              </div>

              <div class="mt-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">审核备注</label>
                <textarea
                  v-model="batchReviewNotes[selectedAppointments[currentReviewIndex]]"
                  rows="3"
                  class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors duration-200"
                  placeholder="请输入审核备注..."
                ></textarea>
              </div>
            </div>
          </div>
          
          <div v-else class="text-center py-8">
            <svg class="mx-auto h-16 w-16 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <h3 class="mt-2 text-lg font-medium text-gray-900">审核完成！</h3>
            <p class="mt-1 text-sm text-gray-500">所有选中的预约已完成审核</p>
            
            <div class="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-100 max-w-md mx-auto">
              <div class="text-sm text-blue-600 font-medium mb-2">分配信息</div>
              <div class="space-y-2 text-left">
                <div class="flex items-center">
                  <svg class="w-5 h-5 text-blue-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span class="text-sm text-gray-700">探访日期：<span class="font-semibold">{{ formatVisitDate(filters.visitDate) }}</span></span>
                </div>
                <div class="flex items-center">
                  <svg class="w-5 h-5 text-blue-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span class="text-sm text-gray-700">时间段：<span class="font-semibold">{{ selectedTimeSlot }}</span></span>
                </div>
                <div class="flex items-center">
                  <svg class="w-5 h-5 text-green-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span class="text-sm text-gray-700">本次分配：<span class="font-semibold text-green-600">{{ approvedCount }} 批</span></span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="border-t border-gray-200 p-4 bg-gray-50">
          <div v-if="selectedAppointments.length > 0 && currentReviewIndex < selectedAppointments.length" class="flex justify-center space-x-3">
            <button 
              @click="handleBatchReject(currentReviewIndex)"
              :disabled="isProcessing"
              class="px-6 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors duration-200 disabled:opacity-70 disabled:cursor-not-allowed"
            >
              拒绝
            </button>
            <button 
              @click="handleBatchApprove(currentReviewIndex)"
              :disabled="isProcessing"
              class="px-6 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 transition-colors duration-200 disabled:opacity-70 disabled:cursor-not-allowed"
            >
              批准
            </button>
          </div>
          
          <div v-else class="flex justify-center space-x-3">
            <button 
              @click="submitBatchReview"
              :disabled="isProcessing"
              class="px-6 py-2 bg-primary text-white rounded-md hover:bg-primary-dark transition-colors duration-200 shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ isProcessing ? '提交中...' : '提交审核结果' }}
            </button>
            <button 
              @click="closeBatchReviewModal"
              class="px-6 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors duration-200"
            >
              取消
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
    const itemsPerPage = ref(50)
    const showRejectModal = ref(false)
    const showBatchReviewModal = ref(false)
    const selectedAppointment = ref(null)
    const rejectReason = ref('')
    const rejectError = ref('')
    const isProcessing = ref(false)
    
    // 批量选择相关
    const selectedAppointments = ref([])
    const timeSlots = ref([
      '09:00-09:40', '09:40-10:20', '10:20-11:00', '11:00-11:40', '15:00-15:40', '15:40-16:20'
    ])
    const selectedTimeSlot = ref(null)
    const currentReviewIndex = ref(0)
    const batchReviewNotes = ref({})
    const approvedCount = ref(0)
    const currentBatchCount = ref(0)
    const batchReviewStatus = ref({})

    // 筛选条件
    const filters = ref({
      status: 'all',
      visitDate: '',
      search: '',
      startDate: '',
      endDate: '',
      sortBy: 'asc'
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

      // 探访日过滤 - 按用户选择的探访日筛选
      if (filters.value.visitDate) {
        result = result.filter(a => {
          if (!a.visitDate) return false
          const visitDate = new Date(a.visitDate)
          const selectedDate = new Date(filters.value.visitDate)
          return visitDate.toDateString() === selectedDate.toDateString()
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

      // 按状态优先级排序，然后按探访日期正序排序，探访日期相同则按提交时间排序
      const statusPriority = {
        'pending': 1,    // 待审核
        'rejected': 2,   // 已拒绝
        'approved': 3,   // 已批准
        'completed': 4   // 已完成
      }
      
      return result.sort((a, b) => {
        const priorityA = statusPriority[a.status] || 999
        const priorityB = statusPriority[b.status] || 999
        
        if (priorityA !== priorityB) {
          return priorityA - priorityB
        }
        
        const visitDateA = a.visitDate ? new Date(a.visitDate).getTime() : Infinity
        const visitDateB = b.visitDate ? new Date(b.visitDate).getTime() : Infinity
        
        if (visitDateA !== visitDateB) {
          return visitDateA - visitDateB
        }
        
        const createTimeA = a.createTime ? new Date(a.createTime).getTime() : 0
        const createTimeB = b.createTime ? new Date(b.createTime).getTime() : 0
        
        if (filters.value.sortBy === 'asc') {
          return createTimeA - createTimeB
        } else {
          return createTimeB - createTimeA
        }
      })
    })

    // 计算每个时间段的预约数量（根据筛选的探访日）
    const timeSlotCounts = computed(() => {
      const counts = {}
      timeSlots.value.forEach(slot => {
        counts[slot] = 0
      })
      
      // 统计已分配到各时间段的预约（状态为approved或completed）
      // 使用所有预约数据，而不是筛选后的数据，确保不受状态筛选影响
      appointments.value.forEach(appointment => {
        // 只统计当前选中的探访日的预约
        if (filters.value.visitDate && appointment.visitDate) {
          const visitDate = new Date(appointment.visitDate)
          const selectedDate = new Date(filters.value.visitDate)
          
          if (visitDate.toDateString() === selectedDate.toDateString()) {
            if ((appointment.status === 'approved' || appointment.status === 'completed') && appointment.time_slot) {
              if (counts.hasOwnProperty(appointment.time_slot)) {
                counts[appointment.time_slot]++
              }
            }
          }
        }
      })
      
      return counts
    })

    // 获取时间段数量颜色类
    const getTimeSlotCountClass = (slot) => {
      const count = timeSlotCounts.value[slot] || 0
      if (count === 0) {
        return 'text-gray-400'
      } else if (count < 20) {
        return 'text-green-600'
      } else {
        return 'text-red-600'
      }
    }

    // 分页相关计算
    const totalPages = computed(() => {
      return Math.ceil(filteredAppointments.value.length / itemsPerPage.value)
    })

    const startIndex = computed(() => {
      return filteredAppointments.value.length === 0 ? 0 : (currentPage.value - 1) * itemsPerPage.value + 1
    })

    const endIndex = computed(() => {
      return Math.min(currentPage.value * itemsPerPage.value, filteredAppointments.value.length)
    })

    // 分页后的数据
    const paginatedAppointments = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value
      const end = start + itemsPerPage.value
      return filteredAppointments.value.slice(start, end)
    })

    // 全选状态计算
    const isAllSelected = computed(() => {
      const pendingAppointments = paginatedAppointments.value.filter(a => a.status === 'pending')
      return pendingAppointments.length > 0 && selectedAppointments.value.length === pendingAppointments.length
    })
    
    // 全选/取消全选
    const toggleSelectAll = () => {
      if (isAllSelected.value) {
        // 取消全选
        selectedAppointments.value = []
      } else {
        // 全选当前页的所有待审核预约
        const pendingIds = paginatedAppointments.value
          .filter(a => a.status === 'pending')
          .map(a => a.id)
        selectedAppointments.value = [...pendingIds]
      }
    }
    
    // 开始批量审核
    const startBatchReview = () => {
      if (selectedAppointments.value.length === 0) {
        alert('请先选择要审核的预约')
        return
      }
      if (!filters.value.visitDate) {
        alert('请先选择探访日')
        return
      }
      if (!selectedTimeSlot.value) {
        alert('请先选择时间段')
        return
      }
      
      // 检查时间段是否已满
      const currentCount = timeSlotCounts.value[selectedTimeSlot.value] || 0
      const newAppointments = selectedAppointments.value.length
      const totalCount = currentCount + newAppointments
      
      if (totalCount > 20) {
        const confirmed = confirm(`当前时间段分配已满（${currentCount}/20），是否继续分配 ${newAppointments} 个预约？\n\n分配后将达到 ${totalCount}/20，超过限制。`)
        if (!confirmed) {
          return
        }
      }
      
      // 重置当前审核索引和备注
      currentReviewIndex.value = 0
      batchReviewNotes.value = {}
      batchReviewStatus.value = {}
      approvedCount.value = 0
      selectedAppointments.value.forEach(id => {
        batchReviewNotes.value[id] = ''
      })
      
      // 计算当前时间段已有的批次数（在弹窗打开时计算）
      currentBatchCount.value = appointments.value.filter(a => 
        a.status === 'approved' || a.status === 'completed'
      ).filter(a => {
        if (!filters.value.visitDate || !a.visitDate) return false
        const visitDate = new Date(a.visitDate)
        const selectedDate = new Date(filters.value.visitDate)
        return visitDate.toDateString() === selectedDate.toDateString() && a.time_slot === selectedTimeSlot.value
      }).length
      
      showBatchReviewModal.value = true
    }
    
    // 处理进度条点击
    const handleProgressBarClick = (event) => {
      const progressBar = event.currentTarget
      const rect = progressBar.getBoundingClientRect()
      const clickX = event.clientX - rect.left
      const width = rect.width
      
      const index = Math.floor((clickX / width) * selectedAppointments.value.length)
      if (index >= 0 && index < selectedAppointments.value.length) {
        currentReviewIndex.value = index
      }
    }
    
    // 获取进度条项的样式类
    const getProgressBarItemClass = (appointmentId, index) => {
      const status = batchReviewStatus.value[appointmentId]
      if (status === 'approved') {
        return 'bg-green-500'
      } else if (status === 'rejected') {
        return 'bg-red-500'
      } else if (index === currentReviewIndex.value) {
        return 'bg-primary'
      } else {
        return 'bg-gray-300'
      }
    }
    
    // 获取审核状态文本
    const getReviewStatusText = (appointmentId) => {
      const status = batchReviewStatus.value[appointmentId]
      if (status === 'approved') return '已批准'
      if (status === 'rejected') return '已拒绝'
      return '待审核'
    }
    
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

    // 格式化探访日期
    const formatVisitDate = (dateString) => {
      if (!dateString) return '请选择探访日'
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
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
      const currentVisitDate = filters.value.visitDate
      filters.value = {
        status: 'all',
        visitDate: currentVisitDate,
        search: '',
        startDate: '',
        endDate: '',
        sortBy: 'asc'
      }
      currentPage.value = 1
    }


    
    // 批准预约 - 自动分配探访日期和时间段
    const handleApprove = async (appointment) => {
      try {
        isProcessing.value = true
        
        // 确认批准
        if (confirm(`确定要批准预约号 ${appointment.appointment_number || appointment.id} 吗？`)) {
          // 调用store action批准预约，不需要手动输入日期和时间，完全由后端自动分配
          const result = await store.dispatch('approveAppointment', {
            id: appointment.id,
            approvalInfo: {
              appointmentNumber: `AP${Date.now()}`,
              receptionLocation: '探访室A',
              receptionist: '值班人员',
              receptionistPhone: '010-12345678'
            }
          })
          
          // 显示自动分配的探访日期和时间段
          const visitDateStr = result.visitDate ? formatDate(result.visitDate) : '待确定';
          alert(`预约已成功批准！\n探访日期：${visitDateStr}\n探访时间：${result.visitTime || '待确定'}`);
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

    // 获取当前审核的预约
    const getCurrentReviewAppointment = computed(() => {
      if (currentReviewIndex.value < 0 || currentReviewIndex.value >= selectedAppointments.value.length) {
        return null
      }
      const appointmentId = selectedAppointments.value[currentReviewIndex.value]
      return appointments.value.find(a => a.id === appointmentId)
    })

    // 批量批准预约
    const handleBatchApprove = async () => {
      if (!selectedTimeSlot.value) {
        alert('请先选择时间段')
        return
      }
      
      const currentAppointment = getCurrentReviewAppointment.value
      if (!currentAppointment) return
      
      // 如果已经审核过，需要确认是否修改
      if (batchReviewStatus.value[currentAppointment.id]) {
        const confirmed = confirm(`该预约已标记为"${getReviewStatusText(currentAppointment.id)}"，是否修改为"批准"？`)
        if (!confirmed) return
      }
      
      try {
        isProcessing.value = true
        
        // 如果之前的状态不是 approved，则增加 approvedCount
        if (batchReviewStatus.value[currentAppointment.id] !== 'approved') {
          approvedCount.value++
        }
        
        // 保存当前审核决策
        batchReviewNotes.value[currentAppointment.id] = batchReviewNotes.value[currentAppointment.id] || ''
        batchReviewStatus.value[currentAppointment.id] = 'approved'
        
        // 移到下一个审核项目
        currentReviewIndex.value++
      } catch (error) {
        alert(`操作失败：${error.message || '请稍后重试'}`)
        console.error('Batch approve error:', error)
      } finally {
        isProcessing.value = false
      }
    }

    // 批量拒绝预约
    const handleBatchReject = async () => {
      const currentAppointment = getCurrentReviewAppointment.value
      if (!currentAppointment) return
      
      const notes = batchReviewNotes.value[currentAppointment.id]
      if (!notes || !notes.trim()) {
        alert('拒绝预约时必须填写审核备注')
        return
      }
      
      // 如果已经审核过，需要确认是否修改
      if (batchReviewStatus.value[currentAppointment.id]) {
        const confirmed = confirm(`该预约已标记为"${getReviewStatusText(currentAppointment.id)}"，是否修改为"拒绝"？`)
        if (!confirmed) return
      }
      
      try {
        isProcessing.value = true
        
        // 如果之前的状态是 approved，则减少 approvedCount
        if (batchReviewStatus.value[currentAppointment.id] === 'approved') {
          approvedCount.value--
        }
        
        // 保存审核状态
        batchReviewStatus.value[currentAppointment.id] = 'rejected'
        
        // 移到下一个审核项目
        currentReviewIndex.value++
      } catch (error) {
        alert(`操作失败：${error.message || '请稍后重试'}`)
        console.error('Batch reject error:', error)
      } finally {
        isProcessing.value = false
      }
    }

    // 关闭批量审核模态框
    const closeBatchReviewModal = () => {
      showBatchReviewModal.value = false
      batchReviewNotes.value = {}
      batchReviewStatus.value = {}
      currentReviewIndex.value = 0
      selectedAppointments.value = []
    }

    // 提交批量审核
    const submitBatchReview = async () => {
      try {
        isProcessing.value = true
        
        // 构建批量审核数据
        const reviewData = []
        approvedCount.value = 0
        selectedAppointments.value.forEach(appointmentId => {
          const appointment = appointments.value.find(a => a.id === appointmentId)
          if (appointment) {
            const notes = batchReviewNotes.value[appointmentId] || ''
            const status = batchReviewStatus.value[appointmentId] || 'approved'
            reviewData.push({
              id: appointmentId,
              status: status,
              approval_notes: notes
            })
            if (status === 'approved') {
              approvedCount.value++
            }
          }
        })
        
        // 调用批量审核API
        await store.dispatch('batchReviewAppointments', {
          appointments: reviewData,
          timeSlot: selectedTimeSlot.value
        })
        
        // 清空选择
        selectedAppointments.value = []
        batchReviewNotes.value = {}
        batchReviewStatus.value = {}
        currentReviewIndex.value = 0
        showBatchReviewModal.value = false
        
        // 刷新数据
        await store.dispatch('initializeData')
        
        // 计算当前时间段的总批次数（在数据刷新后计算）
        currentBatchCount.value = appointments.value.filter(a => 
          a.status === 'approved' || a.status === 'completed'
        ).filter(a => {
          if (!filters.value.visitDate || !a.visitDate) return false
          const visitDate = new Date(a.visitDate)
          const selectedDate = new Date(filters.value.visitDate)
          return visitDate.toDateString() === selectedDate.toDateString() && a.time_slot === selectedTimeSlot.value
        }).length
        
        alert(`批量审核完成！\n\n本次分配：${approvedCount.value} 批\n当前时间段共有：${currentBatchCount.value} 批`)
      } catch (error) {
        alert(`批量审核失败：${error.message || '请稍后重试'}`)
        console.error('Submit batch review error:', error)
      } finally {
        isProcessing.value = false
      }
    }

    // 删除预约
    const handleDelete = async (appointment) => {
      if (confirm(`确定要删除预约号 ${appointment.appointment_number || appointment.id} 吗？此操作不可恢复！`)) {
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
      paginatedAppointments,
      totalPages,
      startIndex,
      endIndex,
      visiblePages,
      showRejectModal,
      showBatchReviewModal,
      rejectReason,
      rejectError,
      isProcessing,
      selectedAppointments,
      selectedTimeSlot,
      timeSlots,
      timeSlotCounts,
      currentReviewIndex,
      batchReviewNotes,
      approvedCount,
      currentBatchCount,
      batchReviewStatus,
      getCurrentReviewAppointment,
      formatDate,
      formatVisitDate,
      formatDateTime,
      getStatusText,
      getStatusClass,
      getTimeSlotCountClass,
      applyFilters,
      resetFilters,
      handleApprove,
      handleReject,
      confirmReject,
      handleComplete,
      exportData,
      handleDelete,
      startBatchReview,
      toggleSelectAll,
      isAllSelected,
      handleBatchApprove,
      handleBatchReject,
      closeBatchReviewModal,
      submitBatchReview,
      handleProgressBarClick,
      getProgressBarItemClass,
      getReviewStatusText
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