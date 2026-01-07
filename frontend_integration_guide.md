# 前端集成指南

本文档提供了如何更新前端界面以支持新的预约流程和查询功能的指导。

## 1. 预约创建页面更新

### 组件示例（AppointmentCreate.vue）

```vue
<template>
  <div class="appointment-create">
    <h2>预约探访</h2>
    <form @submit.prevent="submitAppointment">
      <!-- 探访人信息 -->
      <div class="form-group">
        <label for="name">姓名</label>
        <input type="text" id="name" v-model="formData.name" required>
      </div>
      
      <div class="form-group">
        <label for="id_card">身份证号</label>
        <input type="text" id="id_card" v-model="formData.id_card" required>
      </div>
      
      <div class="form-group">
        <label for="phone_number">联系电话</label>
        <input type="tel" id="phone_number" v-model="formData.phone_number" required>
      </div>
      
      <div class="form-group">
        <label for="relationship">与戒毒人员关系</label>
        <input type="text" id="relationship" v-model="formData.relationship" required>
      </div>
      
      <div class="form-group">
        <label for="visit_reason">探访事由</label>
        <textarea id="visit_reason" v-model="formData.visit_reason" required></textarea>
      </div>
      
      <!-- 亲属信息（可选） -->
      <div v-if="formData.relatives && formData.relatives.length > 0">
        <h3>随行亲属信息</h3>
        <div v-for="(relative, index) in formData.relatives" :key="index">
          <div class="form-group">
            <label>亲属姓名</label>
            <input type="text" v-model="relative.name">
          </div>
          <div class="form-group">
            <label>亲属身份证</label>
            <input type="text" v-model="relative.id_card">
          </div>
          <div class="form-group">
            <label>与戒毒人员关系</label>
            <input type="text" v-model="relative.relationship">
          </div>
        </div>
      </div>
      
      <button type="submit" :disabled="loading">提交预约</button>
    </form>
    
    <!-- 预约结果显示 -->
    <div v-if="appointmentResult" class="result">
      <div class="success-message" v-if="!appointmentResult.error">
        <h3>预约成功！</h3>
        <p>您的预约已成功提交，以下是您的预约信息：</p>
        <ul>
          <li>预约号：{{ appointmentResult.appointment_id }}</li>
          <li>分配月份：{{ appointmentResult.assigned_month_text }}</li>
          <li>预计探访日期：{{ appointmentResult.estimated_visit_date }}</li>
          <li>当前状态：{{ appointmentResult.status === 'pending' ? '待审核' : '排队中' }}</li>
          <li v-if="appointmentResult.status === 'queued'">排队位置：{{ appointmentResult.queue_position }}</li>
        </ul>
      </div>
      <div class="error-message" v-else>
        <h3>预约失败</h3>
        <p>{{ appointmentResult.error }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      formData: {
        name: '',
        id_card: '',
        phone_number: '',
        relationship: '',
        visit_reason: '',
        relatives: []
      },
      loading: false,
      appointmentResult: null
    }
  },
  methods: {
    async submitAppointment() {
      this.loading = true
      this.appointmentResult = null
      
      try {
        const response = await this.$axios.post('/api/appointments/create/', this.formData)
        this.appointmentResult = response.data
        // 重置表单
        this.resetForm()
      } catch (error) {
        this.appointmentResult = {
          error: error.response?.data?.detail || error.message || '预约提交失败，请稍后重试'
        }
      } finally {
        this.loading = false
      }
    },
    resetForm() {
      this.formData = {
        name: '',
        id_card: '',
        phone_number: '',
        relationship: '',
        visit_reason: '',
        relatives: []
      }
    }
  }
}
</script>

<style scoped>
/* 样式定义 */
.appointment-create {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input, textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.result {
  margin-top: 20px;
  padding: 15px;
  border-radius: 4px;
}

.success-message {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}
</style>
```

## 2. 预约排队查询页面

### 组件示例（AppointmentQueue.vue）

```vue
<template>
  <div class="appointment-queue">
    <h2>预约排队查询</h2>
    
    <div v-if="loading" class="loading">加载中...</div>
    
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    
    <div v-else-if="allQueues && allQueues.total_appointments > 0">
      <h3>我的所有预约</h3>
      <div class="queue-list">
        <div 
          v-for="appointment in allQueues.appointments" 
          :key="appointment.appointment_id"
          class="queue-item"
          @click="selectAppointment(appointment.appointment_id)"
        >
          <div class="queue-header">
            <span class="appointment-id">预约号: {{ appointment.appointment_id }}</span>
            <span class="status" :class="appointment.current_status">
              {{ appointment.status_text }}
            </span>
          </div>
          <div class="queue-info">
            <p>分配月份: {{ appointment.assigned_month_text }}</p>
            <p>预计探访日期: {{ appointment.visit_date }}</p>
            <p>排队位置: {{ appointment.queue_position }} / {{ appointment.total_in_queue }}</p>
            <p>已批准预约: {{ appointment.approved_count }} 个</p>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else-if="selectedQueue" class="queue-detail">
      <h3>预约详情</h3>
      <div class="detail-card">
        <div class="detail-item">
          <label>预约号:</label>
          <span>{{ selectedQueue.appointment_id }}</span>
        </div>
        <div class="detail-item">
          <label>分配月份:</label>
          <span>{{ selectedQueue.assigned_month_text }}</span>
        </div>
        <div class="detail-item">
          <label>探访日期:</label>
          <span>{{ selectedQueue.visit_date }}</span>
        </div>
        <div class="detail-item">
          <label>当前状态:</label>
          <span class="status" :class="selectedQueue.current_status">
            {{ selectedQueue.status_text }}
          </span>
        </div>
        <div class="detail-item">
          <label>排队位置:</label>
          <span>{{ selectedQueue.queue_position }} / {{ selectedQueue.total_in_queue }}</span>
        </div>
        <div class="detail-item">
          <label>已批准预约:</label>
          <span>{{ selectedQueue.approved_count }} 个</span>
        </div>
        <div class="detail-item" v-if="selectedQueue.estimated_wait_months > 0">
          <label>预计等待:</label>
          <span>{{ selectedQueue.estimated_wait_months }} 个月</span>
        </div>
      </div>
      <button @click="backToList" class="back-button">返回列表</button>
    </div>
    
    <div v-else class="no-appointments">
      <p>您目前没有正在进行中的预约。</p>
      <router-link to="/appointment/create" class="create-link">创建新预约</router-link>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      allQueues: null,
      selectedQueue: null,
      loading: false,
      error: null
    }
  },
  mounted() {
    this.fetchAllQueues()
  },
  methods: {
    async fetchAllQueues() {
      this.loading = true
      this.error = null
      
      try {
        const response = await this.$axios.get('/api/appointments/queue/')
        this.allQueues = response.data
      } catch (error) {
        this.error = error.response?.data?.error || '获取排队信息失败'
      } finally {
        this.loading = false
      }
    },
    
    async selectAppointment(appointmentId) {
      this.loading = true
      this.error = null
      
      try {
        const response = await this.$axios.get(`/api/appointments/queue/${appointmentId}/`)
        this.selectedQueue = response.data
        this.allQueues = null // 清空列表视图
      } catch (error) {
        this.error = error.response?.data?.error || '获取预约详情失败'
      } finally {
        this.loading = false
      }
    },
    
    backToList() {
      this.selectedQueue = null
      this.fetchAllQueues()
    }
  }
}
</script>

<style scoped>
.appointment-queue {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.loading, .error {
  text-align: center;
  padding: 20px;
}

.error {
  color: #d32f2f;
  background-color: #ffebee;
  border-radius: 4px;
}

.queue-list {
  margin-top: 20px;
}

.queue-item {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.queue-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.queue-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.appointment-id {
  font-weight: bold;
}

.status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.85rem;
}

.status.pending {
  background-color: #fff3cd;
  color: #856404;
}

.status.queued {
  background-color: #e2e3e5;
  color: #383d41;
}

.status.approved {
  background-color: #d4edda;
  color: #155724;
}

.queue-info p {
  margin: 5px 0;
  font-size: 0.9rem;
}

.detail-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-top: 20px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e0e0e0;
}

.detail-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.detail-item label {
  font-weight: bold;
}

.back-button {
  margin-top: 20px;
  padding: 8px 16px;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.no-appointments {
  text-align: center;
  padding: 40px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.create-link {
  display: inline-block;
  margin-top: 15px;
  padding: 8px 16px;
  background-color: #28a745;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}
</style>
```

## 3. API 接口更新

### 新增接口

1. **预约创建** - `/api/appointments/create/`
   - 方法: POST
   - 返回: 包含分配月份、预计探访日期的预约信息

2. **查询所有排队情况** - `/api/appointments/queue/`
   - 方法: GET
   - 返回: 用户所有预约的排队信息

3. **查询单个预约排队情况** - `/api/appointments/queue/<appointment_id>/`
   - 方法: GET
   - 返回: 特定预约的详细排队信息

### 更新的接口

1. **更新预约状态** - `/api/appointments/status/<appointment_id>/`
   - 方法: PUT
   - 添加了每月只能批准一个预约的限制

## 4. 集成步骤

1. 将上述组件添加到您的Vue项目中
2. 更新路由配置，添加新页面的路由
3. 确保axios已正确配置，能够访问后端API
4. 在导航菜单中添加新页面的入口

## 5. 注意事项

1. 确保用户在创建新预约前，没有未完成的预约
2. 显示预约信息时，需要清晰展示分配的月份和排队位置
3. 提供明确的用户反馈，说明预约流程和预计等待时间
4. 对于排队中的用户，定期刷新页面以获取最新的排队状态