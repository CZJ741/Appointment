<template>
  <div class="p-6 relative min-h-screen overflow-hidden">
    <!-- 页面标题 -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">公告管理</h1>
      <p class="mt-1 text-sm text-gray-500">管理和发布系统公告信息</p>
    </div>

    <!-- 操作按钮 -->
    <div class="flex justify-between items-center mb-6">
      <button 
        @click="showAddForm = true"
        class="bg-primary hover:bg-primary-dark text-white font-medium px-4 py-2 rounded-lg transition-colors duration-200 flex items-center"
      >
        <svg class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        发布新公告
      </button>
    </div>

    <!-- 公告列表 -->
    <div class="bg-white rounded-xl shadow-md p-6 mb-8">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                标题
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                发布时间
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                发布机关
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                正文内容
              </th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                操作
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="announcement in announcements" :key="announcement.id" class="hover:bg-gray-50 transition-colors duration-200">
              <td class="px-6 py-4 text-sm font-medium text-gray-900 max-w-xs truncate">
                {{ announcement.title }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(announcement.publishTime) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ announcement.issuingAuthority }}
              </td>
              <td class="px-6 py-4 text-sm text-gray-500 max-w-md truncate">
                {{ announcement.content }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button 
                  @click="editAnnouncement(announcement)"
                  class="text-primary hover:text-primary-dark mr-3 transition-colors duration-200"
                >
                  编辑
                </button>
                <button 
                  @click="deleteAnnouncement(announcement.id)"
                  class="text-red-600 hover:text-red-800 transition-colors duration-200"
                >
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div v-if="announcements.length === 0" class="text-center py-8 text-gray-500">
        暂无公告信息
      </div>
    </div>

    <!-- 添加/编辑公告表单 -->
    <div v-if="showAddForm || editingAnnouncement" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <!-- 表单头部 -->
        <div class="bg-primary text-white px-6 py-4 rounded-t-xl flex justify-between items-center">
          <h2 class="text-xl font-bold">{{ editingAnnouncement ? '编辑公告' : '发布新公告' }}</h2>
          <button 
            @click="closeForm"
            class="text-white hover:text-gray-200 transition-colors duration-200"
          >
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- 表单内容 -->
        <div class="p-6">
          <form @submit.prevent="saveAnnouncement">
            <!-- 标题 -->
            <div class="mb-6">
              <label for="title" class="block text-sm font-medium text-gray-700 mb-2">
                公告标题 <span class="text-red-500">*</span>
              </label>
              <input
                id="title"
                v-model="formData.title"
                type="text"
                class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors duration-200"
                placeholder="请输入公告标题"
                required
              />
            </div>

            <!-- 发布机关 -->
            <div class="mb-6">
              <label for="issuingAuthority" class="block text-sm font-medium text-gray-700 mb-2">
                发布机关 <span class="text-red-500">*</span>
              </label>
              <input
                id="issuingAuthority"
                v-model="formData.issuing_authority"
                type="text"
                class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors duration-200"
                placeholder="请输入发布机关名称"
                required
              />
            </div>

            <!-- 发布时间 -->
            <div class="mb-6">
              <label for="publishTime" class="block text-sm font-medium text-gray-700 mb-2">
                发布时间 <span class="text-red-500">*</span>
              </label>
              <input
                id="publishTime"
                v-model="formData.publish_time"
                type="date"
                class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors duration-200"
                :readonly="editingAnnouncement"
                required
              />
            </div>

            <!-- 公告内容 -->
            <div class="mb-6">
              <label for="content" class="block text-sm font-medium text-gray-700 mb-2">
                公告内容 <span class="text-red-500">*</span>
              </label>
              <textarea
                id="content"
                v-model="formData.content"
                class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary transition-colors duration-200"
                rows="8"
                placeholder="请输入公告内容"
                required
              ></textarea>
            </div>

            <!-- 表单按钮 -->
            <div class="flex justify-end space-x-4">
              <button 
                type="button"
                @click="closeForm"
                class="px-4 py-2 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors duration-200"
              >
                取消
              </button>
              <button 
                type="submit"
                class="bg-primary hover:bg-primary-dark text-white font-medium px-6 py-2 rounded-lg transition-colors duration-200"
              >
                {{ editingAnnouncement ? '保存修改' : '发布公告' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'Announcements',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    // 状态
    const showAddForm = ref(false)
    const editingAnnouncement = ref(null)
    
    // 从Vuex store获取公告数据
    const announcements = computed(() => {
      return store.state.announcements || []
    })
    
    // 表单数据
    const formData = ref({
      title: '',
      publish_time: '',
      content: '',
      issuing_authority: ''
    })
    
    // 页面加载时初始化数据
    onMounted(async () => {
      // 检查是否已登录
      if (!store.state.isAdminLoggedIn) {
        router.push('/admin/login')
        return
      }
      
      // 获取公告数据
      await fetchAnnouncements()
    })
    
    // 获取公告数据
    const fetchAnnouncements = async () => {
      try {
        // 调用后端API获取公告数据
        const response = await axios.get('/announcements/')
        // 更新Vuex状态
        store.commit('SET_ANNOUNCEMENTS', response.data)
      } catch (error) {
        console.error('获取公告数据失败:', error)
        // 出错时不设置数据，保持为空数组
      }
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
    
    // 显示添加公告表单
    const showAddAnnouncementForm = () => {
      showAddForm.value = true
      editingAnnouncement.value = null
      resetForm()
    }
    
    // 编辑公告
    const editAnnouncement = (announcement) => {
      editingAnnouncement.value = announcement
      // 将 publishTime 转换为 YYYY-MM-DD 格式的字符串，以便在日期输入框中正确显示
      const publishDate = new Date(announcement.publishTime)
      const formattedDate = publishDate.toISOString().split('T')[0]
      
      formData.value = {
        title: announcement.title,
        publish_time: formattedDate,
        content: announcement.content,
        issuing_authority: announcement.issuingAuthority
      }
    }
    
    // 删除公告
    const deleteAnnouncement = async (id) => {
      if (confirm('确定要删除这条公告吗？')) {
        try {
          // 调用后端API删除公告
          await axios.delete(`/announcement/${id}/delete/`)
          // 更新本地状态
          announcements.value = announcements.value.filter(announcement => announcement.id !== id)
          store.commit('SET_ANNOUNCEMENTS', announcements.value)
        } catch (error) {
          console.error('删除公告失败:', error)
          alert('删除公告失败，请重试')
        }
      }
    }
    
    // 保存公告
    const saveAnnouncement = async () => {
      try {
        let response;
        let requestData = { ...formData.value };
        
        // 如果是创建新公告，不需要发送publish_time字段（后端会自动设置）
        if (!editingAnnouncement.value) {
          delete requestData.publish_time;
        } else {
          // 如果是编辑公告，需要转换publishTime为正确的格式
          if (requestData.publish_time) {
            requestData.publish_time = new Date(requestData.publish_time).toISOString();
          }
        }
        
        if (editingAnnouncement.value) {
          // 编辑现有公告
          response = await axios.put(`/announcement/${editingAnnouncement.value.id}/update/`, requestData)
        } else {
          // 添加新公告
          response = await axios.post('/announcement/create/', requestData)
        }
        
        // 重新获取最新的公告数据
        await fetchAnnouncements()
        
        // 关闭表单
        closeForm()
      } catch (error) {
        console.error('保存公告失败:', error)
        alert('保存公告失败，请重试')
      }
    }
    
    // 关闭表单
    const closeForm = () => {
      showAddForm.value = false
      editingAnnouncement.value = null
      resetForm()
    }
    
    // 重置表单
    const resetForm = () => {
      formData.value = {
        title: '',
        publish_time: '',
        content: '',
        issuing_authority: ''
      }
    }
    
    return {
      announcements,
      showAddForm,
      editingAnnouncement,
      formData,
      formatDate,
      editAnnouncement,
      deleteAnnouncement,
      saveAnnouncement,
      closeForm
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

/* 表格行悬停效果增强 */
tbody tr:hover {
  background-color: rgba(249, 250, 251, 0.8);
}
</style>