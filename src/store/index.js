import { createStore } from 'vuex'
import { getLoginStatus, logoutAdmin, validateAdminLogin } from '../utils/auth.js'
import axios from 'axios'

// 配置axios基础URL
axios.defaults.baseURL = '/api'

// 请求拦截器，添加token
axios.interceptors.request.use(config => {
  // 确保headers对象存在
  if (!config.headers) {
    config.headers = {}
  }
  
  // 管理员接口(/appointment/all/)不需要token，只有普通用户接口需要token
  if (!(config.url && config.url.includes('/appointment/all/'))) {
    // 普通用户接口，使用user_token
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
        // 对于普通用户，后端返回的数据已经是过滤后的，直接返回所有数据
        return state.appointments
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
          const { approvalInfo, visitDate, month, ...otherData } = data
          
          // 特殊处理特定属性
          if (approvalInfo) {
            state.appointments[index].approvalInfo = approvalInfo
          }
          if (visitDate) {
            state.appointments[index].visitDate = visitDate
          }
          if (month) {
            state.appointments[index].month = month
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
            // 不抛出错误，继续执行
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
            // 时间处理
            visitDate: appointment.appointment_time,
            visitTime: appointment.appointment_time ? new Date(appointment.appointment_time).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }) : '',
            createTime: appointment.created_at || new Date().toISOString(),
            // 月份处理
            month: appointment.appointment_time ? 
              `${new Date(appointment.appointment_time).getFullYear()}-${String(new Date(appointment.appointment_time).getMonth() + 1).padStart(2, '0')}` : 
              `${new Date().getFullYear()}-${String(new Date().getMonth() + 1).padStart(2, '0')}`,
            // 直接映射其他必要字段
            visitorAddress: appointment.visitor_address || '',
            prisonerName: appointment.prisoner_name || '',
            appointmentReason: appointment.appointment_reason || '',
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
    async approveAppointment({ commit }, { id, approvalData, visitDate, targetMonth }) {
      try {
        // 调用后端API批准预约
         const response = await axios.put(`/appointment/${id}/approve/`, {
          approvalData,
          visitDate,
          targetMonth
        })
        
        const updatedAppointment = response.data
        commit('UPDATE_APPOINTMENT_STATUS', {
          id,
          status: 'approved',
          data: updatedAppointment
        })
        
        return updatedAppointment
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
    // 管理员登录
    async adminLogin({ commit }, credentials) {
      try {
        // 使用前端模拟登录进行验证（传递第三个参数captcha，这里使用空字符串）
        const loginResult = await validateAdminLogin(credentials.username, credentials.password, '')
        
        if (loginResult.success) {
          // 保存登录状态和token
          localStorage.setItem('admin_token', 'admin_mock_token')
          localStorage.setItem('admin_user', JSON.stringify(loginResult.user))
          
          commit('SET_ADMIN_LOGIN', {
            isLoggedIn: true,
            user: loginResult.user
          })
          
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

    // 用户登录（新的用户名密码系统）
    async userLogin({ commit }, credentials) {
      try {
        // 调用后端API进行用户登录
        const response = await axios.post('/login/', credentials)
        
        const { token, user_id, username, full_name } = response.data
        const user = {
          id: user_id,
          username: username,
          full_name: full_name
        }
        commit('SET_USER_LOGIN', { user, token })
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