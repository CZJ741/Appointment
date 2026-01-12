import { createStore } from 'vuex'
import { getLoginStatus, logoutAdmin, validateAdminLogin } from '../utils/auth.js'
import axios from 'axios'

// 配置axios基础URL
axios.defaults.baseURL = 'http://apb.vgit.cn/api'
// http://127.0.0.1:8000
// 请求拦截器，添加token
axios.interceptors.request.use(config => {
  // 确保headers对象存在
  if (!config.headers) {
    config.headers = {}
  }
  
  // 判断是否为管理员接口
  const isAdminApi = config.url && (
    config.url.includes('/appointment/all/') ||
    config.url.includes('/appointment/batch-review/') ||
    (config.url.includes('/appointment/') && 
    (config.url.includes('/approve/') || config.url.includes('/reject/') || 
     (config.url.includes('/detail/') && !config.url.includes('/cancel/')) || 
     config.url.includes('/complete/'))) ||
    // 公告相关接口
    config.url.includes('/announcement/create/') ||
    config.url.includes('/announcement/') && config.url.includes('/update/') ||
    config.url.includes('/announcement/') && config.url.includes('/delete/')
  )
  
  // 根据接口类型添加相应的token
  if (isAdminApi) {
    // 管理员接口添加管理员token
    const adminToken = localStorage.getItem('admin_token')
    if (adminToken) {
      config.headers.Authorization = `Token ${adminToken}`
    }
  } else {
    // 普通用户接口添加用户token
    const userToken = localStorage.getItem('user_token')
    if (userToken) {
      config.headers.Authorization = `Token ${userToken}`
    }
  }
  
  console.log('请求URL:', config.url)
  console.log('请求头:', config.headers)
  return config
}, error => {
  console.error('请求拦截器错误:', error)
  return Promise.reject(error)
})




export default createStore({
  state: {
    appointments: [],
    currentAppointment: null,
    isAdminLoggedIn: !!localStorage.getItem('admin_token'),
    adminInfo: null,
    // 公告数据
    announcements: [],
    // 用户登录状态
    user: {
      isLoggedIn: !!localStorage.getItem('user_token'),
      info: (() => {
        const userInfo = localStorage.getItem('user_info');
        if (userInfo && userInfo !== 'undefined') {
          try {
            return JSON.parse(userInfo);
          } catch (e) {
            console.warn('解析user_info时出错:', e);
            return null;
          }
        }
        console.warn('user_info为空或为"undefined"字符串');
        return null;
      })(),
      token: localStorage.getItem('user_token') || null
    }
  },
  getters: {
    // 按状态筛选预约
    pendingAppointments: (state) => {
      return state.appointments.filter(appt => appt.status === 'pending')
    },
    approvedAppointments: (state) => {
      return state.appointments.filter(appt => appt.status === 'approved')
    },
    rejectedAppointments: (state) => {
      return state.appointments.filter(appt => appt.status === 'rejected')
    },
    completedAppointments: (state) => {
      return state.appointments.filter(appt => appt.status === 'completed')
    },
    // 获取指定月份的预约
    getAppointmentsByMonth: (state) => (month) => {
      return state.appointments.filter(appt => appt.month === month)
    },
    // 获取预约详情
    getAppointmentById: (state) => (id) => {
      // 处理可能的类型不匹配问题，确保能正确找到预约记录
      return state.appointments.find(appt => String(appt.id) === String(id))
    },
    // 用户是否已登录
    isUserLoggedInByUsername: (state) => state.user && state.user.isLoggedIn,
    
    // 获取用户的所有预约
    userAppointments: (state) => {
      if (state.user && state.user.isLoggedIn) {
        // 即使后端返回了所有数据，也要在前端额外过滤，确保只显示当前用户的预约
        return state.appointments.filter(appointment => {
          // 检查appointment是否包含user_info字段，并且user_info.id与当前用户id匹配
          return appointment.user_info && appointment.user_info.id === state.user.info.id
        })
      }
      return []
    },
    
    // 获取用户在特定月份的预约
    userAppointmentsByMonth: (state) => (month) => {
      if (state.user && state.user.isLoggedIn && state.user.info) {
        // 使用用户系统
        return state.appointments.filter(appointment => 
          appointment.userId === state.user.info.id && appointment.month === month
        )
      }
      return []
    },
    
    // 获取当前月份的批次情况
    currentMonthBatchInfo: (state) => {
      const now = new Date()
      const currentMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
      const currentMonthAppointments = state.appointments.filter(a => a.month === currentMonth)
      
      // 查找已批准的批次
      const approvedBatches = currentMonthAppointments
        .filter(a => a.status === 'approved')
        .map(a => a.batchNumber)
        .filter((value, index, self) => self.indexOf(value) === index)
      
      return {
        month: currentMonth,
        hasApprovedBatch: approvedBatches.length > 0,
        totalPending: currentMonthAppointments.filter(a => a.status === 'pending').length
      }
    },
    
    // 获取预约的排队位置
    appointmentQueuePosition: (state) => (appointmentId) => {
      const appointment = state.appointments.find(a => a.id === appointmentId)
      if (!appointment) return null
      
      // 查找同月份中，创建时间早于当前预约的待审核预约数量
      const earlierPending = state.appointments.filter(a => 
        a.month === appointment.month && 
        a.status === 'pending' && 
        new Date(a.createTime) < new Date(appointment.createTime)
      ).length
      
      return earlierPending + 1
    }
  },
  mutations: {
    // 初始化数据
    INIT_DATA(state, data) {
      state.appointments = data
    },
    // 添加新预约
    ADD_APPOINTMENT(state, appointment) {
      state.appointments.push(appointment)
    },
    // 更新预约状态
    UPDATE_APPOINTMENT_STATUS(state, { id, status, data }) {
      const index = state.appointments.findIndex(appt => appt.id === id)
      if (index !== -1) {
        state.appointments[index].status = status
        if (data) {
          // 先移除会被特殊处理的属性
          const { approvalInfo, visitDate, month, visitTime, ...otherData } = data
          
          // 特殊处理特定属性
          if (approvalInfo) {
            state.appointments[index].approvalInfo = approvalInfo
            // 确保visitTime从approvalInfo中正确设置
            if (approvalInfo.receptionTime) {
              state.appointments[index].visitTime = approvalInfo.receptionTime
            }
          }
          if (visitDate) {
            state.appointments[index].visitDate = visitDate
          }
          if (month) {
            state.appointments[index].month = month
          }
          // 直接设置visitTime（如果有）
          if (visitTime) {
            state.appointments[index].visitTime = visitTime
          }
          
          // 合并其他属性
          Object.assign(state.appointments[index], otherData)
        }
      }
    },
    // 设置当前预约
    SET_CURRENT_APPOINTMENT(state, appointment) {
      state.currentAppointment = appointment
    },
    // 设置管理员登录状态
    SET_ADMIN_LOGIN(state, { user, isLoggedIn }) {
      state.isAdminLoggedIn = isLoggedIn
      state.adminInfo = user
    },
    // 设置管理员信息
    SET_ADMIN_INFO(state, info) {
      state.adminInfo = info
    },
    // 初始化登录状态
    INIT_LOGIN_STATUS(state) {
      const status = getLoginStatus()
      state.isAdminLoggedIn = status.loggedIn
      state.adminInfo = status.user || null
    },
    // 删除预约
    DELETE_APPOINTMENT(state, id) {
      const index = state.appointments.findIndex(appt => appt.id === id)
      if (index !== -1) {
        state.appointments.splice(index, 1)
      }
    },

    // 设置用户登录状态
    SET_USER_LOGIN(state, { user, token }) {
      state.user = {
        isLoggedIn: true,
        info: user,
        token: token
      }
      localStorage.setItem('user_token', token)
      localStorage.setItem('user_info', JSON.stringify(user))
    },
    // 清除用户登录状态
    CLEAR_USER_LOGIN(state) {
      state.user = {
        isLoggedIn: false,
        info: null,
        token: null
      }
      localStorage.removeItem('user_token')
      localStorage.removeItem('user_info')
    },
    // 设置公告列表
    SET_ANNOUNCEMENTS(state, announcements) {
      // 将后端返回的snake_case字段转换为前端使用的camelCase
      state.announcements = announcements.map(announcement => ({
        ...announcement,
        publishTime: announcement.publish_time,
        issuingAuthority: announcement.issuing_authority
      }))
    },
    // 添加新公告
    ADD_ANNOUNCEMENT(state, announcement) {
      state.announcements.push(announcement)
    },
    // 更新公告
    UPDATE_ANNOUNCEMENT(state, announcement) {
      const index = state.announcements.findIndex(a => a.id === announcement.id)
      if (index !== -1) {
        state.announcements[index] = announcement
      }
    },
    // 删除公告
    DELETE_ANNOUNCEMENT(state, id) {
      state.announcements = state.announcements.filter(announcement => announcement.id !== id)
    }
  },
  actions: {
    // 初始化应用数据（异步实现）
    async initializeData({ commit, state }) {
      try {
        console.log('初始化数据开始，用户登录状态:', state.user.isLoggedIn);
        // 调用后端API获取预约数据
        let appointmentData = [];
        let response;
        
        if (state.isAdminLoggedIn) {
          try {
            // 移除管理员token设置
            response = await axios.get('/appointment/all/');
            appointmentData = response.data;
            console.log('管理员数据获取成功');
          } catch (error) {
            console.error('获取所有预约数据失败:', error);
            // 管理员获取数据失败时，直接返回空数组，不尝试获取个人预约数据
            appointmentData = [];
          }
        } else if (state.user.isLoggedIn) {
          try {
            console.log('正在获取用户预约数据');
            response = await axios.get('/appointment/my/');
            appointmentData = response.data;
            console.log('用户预约数据获取成功:', appointmentData);
          } catch (error) {
            console.error('获取个人预约数据失败:', error);
            // 不抛出错误，继续执行
            appointmentData = [];
          }
        } else {
          console.log('用户未登录，不获取数据');
        }
        
        // 确保appointmentData是数组格式
        let appointmentsData = Array.isArray(appointmentData) ? appointmentData : [];
        
        // 转换数据格式，确保与前端组件期望的结构匹配
        appointmentsData = appointmentsData.map(appointment => {
          // 构建主要探访人信息
          const primaryVisitor = {
            name: appointment.visitor_name || '',
            gender: appointment.visitor_gender || '',
            idCard: appointment.visitor_id_card || '',
            phone: appointment.visitor_phone || '',
            relationship: appointment.relationship || ''
          };
          
          // 构建visitors数组，包含主要探访人和额外亲属
          let visitors = [primaryVisitor];
          
          // 添加额外的亲属信息（如果有）
          if (appointment.relatives && Array.isArray(appointment.relatives)) {
            const relativeVisitors = appointment.relatives.map(relative => ({
              name: relative.name || '',
              gender: relative.gender || '',
              idCard: relative.id_card || '',
              phone: relative.phone || '',
              relationship: relative.relationship || ''
            }));
            visitors = [...visitors, ...relativeVisitors];
          }
          
          // 转换后端数据格式为前端期望的格式
          return {
            id: appointment.id,
            // 完整的visitors数组
            visitors: visitors,
            // 状态映射
            status: appointment.status || 'pending',
            // 时间处理 - visitDate使用用户选择的探访日期
            visitDate: appointment.visit_date,
            visitTime: appointment.time_slot || '',
            createTime: appointment.created_at || new Date().toISOString(),
            // 月份处理 - 使用visit_date的月份
            month: appointment.visit_date ? 
              `${new Date(appointment.visit_date).getFullYear()}-${String(new Date(appointment.visit_date).getMonth() + 1).padStart(2, '0')}` : 
              `${new Date().getFullYear()}-${String(new Date().getMonth() + 1).padStart(2, '0')}`,
            // 直接映射其他必要字段
            visitorAddress: appointment.visitor_address || '',
            prisonerName: appointment.prisoner_name || '',
            appointmentReason: appointment.appointment_reason || '',
            approvalNotes: appointment.approval_notes || '',
            // 保留其他原始字段
            ...appointment
          };
        });
        
        commit('INIT_DATA', appointmentsData)
        console.log('成功从后端API加载数据并转换格式', appointmentsData)
        return Promise.resolve()
      } catch (error) {
        console.error('初始化数据失败:', error)
        // 即使出错也要返回空数组，确保应用不会崩溃
        commit('INIT_DATA', [])
        // 返回resolve而不是reject，避免未处理的Promise拒绝
        return Promise.resolve()
      }
    },
    
    // 检查当月是否有可用批次（一个月只能有一个预约）
    async checkMonthAvailability() {
      try {
        // 后端暂未实现此接口，返回模拟数据
        // 假设当前月份总是可用
        return true
      } catch (error) {
        console.error('检查月份可用性失败:', error)
        // 出错时默认可用，让用户可以继续尝试
        return true
      }
    },
    
    // 获取下一个可用月份
    async getNextAvailableMonth() {
      try {
        // 后端暂未实现此接口，返回模拟数据
        const now = new Date()
        const nextMonth = new Date(now.getFullYear(), now.getMonth() + 1, 1)
        return `${nextMonth.getFullYear()}-${String(nextMonth.getMonth() + 1).padStart(2, '0')}`
      } catch (error) {
        console.error('获取下一个可用月份失败:', error)
        const now = new Date()
        const nextMonth = new Date(now.getFullYear(), now.getMonth() + 1, 1)
        return `${nextMonth.getFullYear()}-${String(nextMonth.getMonth() + 1).padStart(2, '0')}`
      }
    },
    
    // 创建新预约
    async createAppointment({ commit }, appointmentData) {
      try {
        // 调用后端API创建预约
         const response = await axios.post('/appointment/create/', appointmentData)
        
        const newAppointment = response.data
        commit('ADD_APPOINTMENT', newAppointment)
        return newAppointment
      } catch (error) {
        console.error('创建预约失败:', error)
        throw error.response?.data?.detail || error.message
      }
    },
    // 审批预约
    async approveAppointment({ commit }, { id, approvalInfo }) {
      try {
        // 添加日志以调试
        console.log('approveAppointment参数:', {
          id,
          receptionTime: approvalInfo?.receptionTime
        })
        
        // 调用后端API批准预约，不传递手动选择的日期和时间，由后端自动分配
         const response = await axios.put(`/appointment/${id}/approve/`, {
          approvalInfo
        })
        
        console.log('API响应:', response.data)
        
        // 创建更新数据，使用后端返回的日期和时间
        const updateData = {
          ...response.data,
          visitTime: response.data.time_slot || '',
          visitDate: response.data.visit_date
        }
        
        commit('UPDATE_APPOINTMENT_STATUS', {
          id,
          status: 'approved',
          data: updateData
        })
        
        return updateData
      } catch (error) {
        console.error('批准预约失败:', error)
        throw error.response?.data?.detail || error.message
      }
    },
    // 拒绝预约
    async rejectAppointment({ commit }, { id, reason }) {
      try {
        // 调用后端API拒绝预约
         await axios.put(`/appointment/${id}/reject/`, { reason })
        
        commit('UPDATE_APPOINTMENT_STATUS', {
          id,
          status: 'rejected',
          data: { rejectionReason: reason }
        })
      } catch (error) {
        console.error('拒绝预约失败:', error)
        throw error.response?.data?.detail || error.message
      }
    },
    // 标记完成
    async completeAppointment({ commit }, { id, notes }) {
      try {
        // 调用后端API标记预约完成
         await axios.put(`/appointment/${id}/complete/`, { notes })
        
        commit('UPDATE_APPOINTMENT_STATUS', {
          id,
          status: 'completed',
          data: { completionNotes: notes }
        })
      } catch (error) {
        console.error('标记预约完成失败:', error)
        throw error.response?.data?.detail || error.message
      }
    },
    // 删除预约
    async deleteAppointment({ commit }, id) {
      try {
        // 调用后端API删除预约
         await axios.delete(`/appointment/detail/${id}/`)
        commit('DELETE_APPOINTMENT', id)
      } catch (error) {
        console.error('删除预约失败:', error)
        throw error.response?.data?.detail || error.message
      }
    },
    // 取消预约
    async cancelAppointment({ commit }, id) {
      try {
        // 调用后端API取消预约，使用与批准/拒绝相同的路径模式
        const response = await axios.put(`/appointment/${id}/cancel/`)
        
        // 从本地状态中删除该预约记录
        commit('DELETE_APPOINTMENT', id)
        
        return response.data
      } catch (error) {
        console.error('取消预约失败:', error)
        throw error.response?.data?.detail || error.message
      }
    },
    // 批量审核预约
    async batchReviewAppointments({ commit }, { appointments, timeSlot }) {
      try {
        // 构建请求数据
        const requestData = {
          appointments: appointments.map(appt => ({
            id: appt.id,
            status: appt.status,
            time_slot: appt.status === 'approved' ? timeSlot : undefined,
            approval_notes: appt.approval_notes
          }))
        }
        
        console.log('批量审核请求数据:', requestData)
        
        // 调用后端批量审核API
        const response = await axios.post('/appointment/batch-review/', requestData)
        
        console.log('批量审核API响应:', response.data)
        
        // 更新本地状态
        response.data.results.forEach(result => {
          if (result.status === 'success') {
            const appointmentData = appointments.find(a => a.id === result.id)
            if (appointmentData) {
              commit('UPDATE_APPOINTMENT_STATUS', {
                id: result.id,
                status: appointmentData.status,
                data: {
                  time_slot: appointmentData.status === 'approved' ? timeSlot : undefined,
                  approval_notes: appointmentData.approval_notes
                }
              })
            }
          }
        })
        
        return response.data
      } catch (error) {
        console.error('批量审核失败:', error)
        throw error.response?.data?.error || error.message
      }
    },
    // 管理员登录
    async adminLogin({ commit }, credentials) {
      try {
        // 使用前端模拟登录进行验证（传递第三个参数captcha，这里使用空字符串）
        const loginResult = await validateAdminLogin(credentials.username, credentials.password, '')
        
        if (loginResult.success) {
          // 管理员登录时，清除客户端用户登录状态
          localStorage.removeItem('user_token')
          localStorage.removeItem('user_info')
          
          // 保存登录状态和token
          localStorage.setItem('admin_token', loginResult.token)
          localStorage.setItem('admin_user', JSON.stringify(loginResult.user))
          
          // 设置管理员登录状态
          commit('SET_ADMIN_LOGIN', {
            isLoggedIn: true,
            user: loginResult.user
          })
          
          // 清除客户端用户登录状态
          commit('CLEAR_USER_LOGIN')
          
          return true
        } else {
          // 出错时重置登录状态
          commit('SET_ADMIN_LOGIN', {
            isLoggedIn: false,
            user: null
          })
          throw new Error(loginResult.message || '登录失败')
        }
      } catch (error) {
        console.error('Login error:', error)
        // 出错时重置登录状态
        localStorage.removeItem('admin_token')
        localStorage.removeItem('admin_user')
        commit('SET_ADMIN_LOGIN', {
          isLoggedIn: false,
          user: null
        })
        return false
      }
    },
    // 管理员登出
    async adminLogout({ commit }) {
      try {
        // 只执行前端登出逻辑，清除本地存储和状态
        // 清除token和用户信息
        localStorage.removeItem('admin_token')
        localStorage.removeItem('admin_user')
        
        commit('SET_ADMIN_LOGIN', {
          isLoggedIn: false,
          user: null
        })
      } catch (error) {
        console.error('Logout error:', error)
        // 即使出错也要清除本地状态
        localStorage.removeItem('admin_token')
        localStorage.removeItem('admin_user')
        commit('SET_ADMIN_LOGIN', {
          isLoggedIn: false,
          user: null
        })
      }
    },
    // 初始化登录状态
    async initializeLoginStatus({ commit }) {
      commit('INIT_LOGIN_STATUS')
    },

    // 用户注册（新的用户名密码系统）
    async userRegister({ commit }, registrationData) {
      try {
        // 将前端的confirmPassword字段映射到后端需要的password_confirm字段
        const requestData = {
          ...registrationData,
          password_confirm: registrationData.confirmPassword,
          // 移除原始的confirmPassword字段
          confirmPassword: undefined
        }
        // 调用后端API进行用户注册
        const response = await axios.post('/register/', requestData)
        
        // 返回成功结果
        return { success: true, data: response.data }
      } catch (error) {
        console.error('用户注册失败:', error)
        // 返回错误信息，保持与login接口一致的错误处理格式
        return { 
          success: false, 
          error: error.response?.data || { message: error.message || '注册失败，请稍后重试' } 
        }
      }
    },
    
    // 用户登录（新的用户名密码系统）
    async userLogin({ commit }, credentials) {
      try {
        // 客户端用户登录时，清除管理员登录状态
        localStorage.removeItem('admin_token')
        localStorage.removeItem('admin_user')
        
        // 设置管理员登录状态为未登录
        commit('SET_ADMIN_LOGIN', {
          isLoggedIn: false,
          user: null
        })
        
        // 调用后端API进行用户登录
        const response = await axios.post('/login/', credentials)
        
        const { token, user_id, username, full_name } = response.data
        const user = {
          id: user_id,
          username: username,
          full_name: full_name
        }
        commit('SET_USER_LOGIN', { user, token })
        
        // 登录成功后，检查预约审核状态
        try {
          const appointmentsResponse = await axios.get('/appointment/my/')
          const appointments = appointmentsResponse.data || []
          
          // 查找最新的已批准或已拒绝的预约
          const approvedAppointment = appointments
            .filter(app => app.status === 'approved')
            .sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at))[0]
          
          const rejectedAppointment = appointments
            .filter(app => app.status === 'rejected')
            .sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at))[0]
          
          // 如果有已批准的预约，显示提示
          if (approvedAppointment) {
            const visitDate = approvedAppointment.visit_date
            const timeSlot = approvedAppointment.time_slot
            setTimeout(() => {
              alert(`您的预约已审核通过！\n探访日期：${visitDate}\n探访时间：${timeSlot}`)
            }, 500)
          }
          
          // 如果有已拒绝的预约，显示提示
          if (rejectedAppointment) {
            const rejectionReason = rejectedAppointment.rejection_reason || '请于“我的预约” 界面查看'
            setTimeout(() => {
              alert(`您的预约审核未通过！\n拒绝原因：${rejectionReason}`)
            }, 500)
          }
        } catch (error) {
          console.error('获取预约状态失败:', error)
          // 不影响登录流程，继续执行
        }
        
        return { success: true }
      } catch (error) {
        console.error('用户登录失败:', error)
        throw error.response?.data?.detail || error.message
      }
    },
    // 用户登出（新的用户名密码系统）
    async userLogout({ commit }) {
      try {
        // 调用后端API进行用户登出
        await axios.post('/logout/')
        commit('CLEAR_USER_LOGIN')
      } catch (error) {
        console.error('用户登出失败:', error)
        // 即使出错也要清除本地状态
        commit('CLEAR_USER_LOGIN')
        throw error.response?.data?.detail || error.message
      }
    }
  },
  modules: {}
})