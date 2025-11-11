import { createStore } from 'vuex'
import { getLoginStatus, logoutAdmin } from '../utils/auth.js'




export default createStore({
  state: {
    appointments: [],
    currentAppointment: null,
    isAdminLoggedIn: !!localStorage.getItem('admin_token'),
    adminInfo: null,
    userWxid: localStorage.getItem('user_wxid') || null
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
      return state.appointments.find(appt => appt.id === id)
    },
    // 用户是否已登录
    isUserLoggedIn: (state) => !!state.userWxid,
    
    // 获取用户的所有预约
    userAppointments: (state) => {
      if (!state.userWxid) return []
      return state.appointments.filter(appointment => appointment.wxid === state.userWxid)
    },
    
    // 获取用户在特定月份的预约
    userAppointmentsByMonth: (state) => (month) => {
      if (!state.userWxid) return []
      return state.appointments.filter(appointment => 
        appointment.wxid === state.userWxid && appointment.month === month
      )
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
      localStorage.setItem('appointments', JSON.stringify(state.appointments))
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
        localStorage.setItem('appointments', JSON.stringify(state.appointments))
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
        localStorage.setItem('appointments', JSON.stringify(state.appointments))
      }
    },
    // 设置用户wxid
    SET_USER_WXID(state, wxid) {
      state.userWxid = wxid
      localStorage.setItem('user_wxid', wxid)
    },
    // 清除用户wxid
    CLEAR_USER_WXID(state) {
      state.userWxid = null
      localStorage.removeItem('user_wxid')
    }
  },
  actions: {
    // 初始化应用数据（异步实现）
    async initializeData({ commit }) {
      try {
        // 尝试从localStorage加载数据
        const storedData = localStorage.getItem('appointments')
        
        if (storedData) {
          try {
            // 解析存储的数据
            const parsedData = JSON.parse(storedData)
            commit('INIT_DATA', parsedData)
            console.log('成功从localStorage加载数据')
          } catch (parseError) {
            console.error('解析存储数据失败:', parseError)
            // 解析失败时只返回空数组，不生成测试数据
            commit('INIT_DATA', [])
            // 清空损坏的数据
            localStorage.setItem('appointments', JSON.stringify([]))
          }
        } else {
          // localStorage中没有数据时，返回空数组，不生成模拟数据
          console.log('localStorage中没有数据，使用空数组初始化')
          commit('INIT_DATA', [])
          localStorage.setItem('appointments', JSON.stringify([]))
        }
        
        return Promise.resolve()
      } catch (error) {
        console.error('初始化数据失败:', error)
        // 即使出错也要返回空数组，确保应用不会崩溃
        commit('INIT_DATA', [])
        return Promise.reject(error)
      }
    },
    
    // 检查当月是否有可用批次（一个月只能有一个预约）
    checkMonthAvailability({ state }) {
      const now = new Date()
      const currentMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
      // 只要该月有已批准的预约，就认为批次已满
      return state.appointments.filter(a => a.month === currentMonth && a.status === 'approved').length === 0
    },
    
    // 获取下一个可用月份
    getNextAvailableMonth({ state }) {
      const now = new Date()
      let monthToCheck = new Date(now)
      
      // 最多检查未来12个月
      for (let i = 0; i < 12; i++) {
        const checkMonth = `${monthToCheck.getFullYear()}-${String(monthToCheck.getMonth() + 1).padStart(2, '0')}`
        // 检查该月是否已有已批准的预约
        const hasApprovedAppointment = state.appointments.some(a => a.month === checkMonth && a.status === 'approved')
        
        if (!hasApprovedAppointment) {
          return checkMonth
        }
        
        // 检查下一个月
        monthToCheck = new Date(monthToCheck)
        monthToCheck.setMonth(monthToCheck.getMonth() + 1)
      }
      
      return null
    },
    
    // 创建新预约 - 不分配具体日期，只分配月份供排队使用
    createAppointment({ commit, state }, { appointmentData, wxid }) {
      const now = new Date()
      const targetMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
      
      // 检查该月份是否已有已批准的预约（一个月只能有一个批次）
      const hasApprovedAppointment = state.appointments.some(a => 
        a.month === targetMonth && a.status === 'approved'
      )
      
      if (hasApprovedAppointment) {
        throw new Error(`月份 ${targetMonth} 已有批准的预约批次，请在下个月尝试创建预约。`)
      }
      
      // 计算该月待审核预约的数量作为队列号
      const pendingInMonth = state.appointments.filter(a => 
        a.month === targetMonth && a.status === 'pending'
      ).length
      const queueNumber = pendingInMonth + 1
      
      // 创建预约时不分配具体探访日期，日期将在管理员审核时指定
      let visitDate = null;
      
      const newAppointment = {
          id: `appt-${Date.now()}`,
          month: targetMonth,
          wxid: wxid,
          visitDate: visitDate,
          visitTime: '09:00',
          queueNumber: queueNumber,
          batchNumber: 1, // 每月只有一个批次
          status: 'pending',
          createTime: new Date().toISOString(),
          visitors: appointmentData.visitors,
          patientName: appointmentData.patientName || '',
          applicantAddress: appointmentData.applicantAddress || '',
          rejectionReason: '',
          approvalInfo: null,
          completionNotes: ''
        }
      
      commit('ADD_APPOINTMENT', newAppointment)
      return newAppointment
    },
    // 审批预约 - 必须传入具体的探访日期，同时支持指定目标月份
    approveAppointment({ commit, state }, { id, approvalData, visitDate, targetMonth }) {
      // 获取要审批的预约
      const appointment = state.appointments.find(a => a.id === id)
      if (!appointment) {
        throw new Error('预约不存在')
      }
      
      // 验证必须提供探访日期
      if (!visitDate) {
        throw new Error('必须提供具体的探访日期才能批准预约。')
      }
      
      let finalVisitDate = visitDate
      
      // 根据探访日期确定月份（格式化为YYYY-MM）
      const visitDateObj = new Date(finalVisitDate)
      const monthToUse = targetMonth || `${visitDateObj.getFullYear()}-${String(visitDateObj.getMonth() + 1).padStart(2, '0')}`
      
      // 确保targetMonth与探访日期的月份一致
      if (targetMonth) {
        const targetMonthObj = new Date(targetMonth + '-01')
        if (visitDateObj.getFullYear() !== targetMonthObj.getFullYear() || 
            visitDateObj.getMonth() !== targetMonthObj.getMonth()) {
          throw new Error('探访日期必须与指定的目标月份一致。')
        }
      }
      
      // 检查探访日期是否已被其他已批准的预约使用
      const hasDateConflict = state.appointments.some(a => 
        a.id !== id && // 排除当前正在审批的预约
        a.status === 'approved' && // 只检查已批准的预约
        a.data?.visitDate === finalVisitDate // 日期冲突检查
      )
      
      if (hasDateConflict) {
        throw new Error(`日期 ${finalVisitDate} 已被其他预约占用，请选择其他日期。`)
      }
      
      // 检查该月份是否已有已批准的预约（一个月只能有一个批次）
      const hasMonthConflict = state.appointments.some(a => 
        a.id !== id && // 排除当前正在审批的预约
        a.status === 'approved' && // 只检查已批准的预约
        a.month === monthToUse // 月份冲突检查（使用确定的月份）
      )
      
      if (hasMonthConflict) {
        throw new Error(`月份 ${monthToUse} 已有批准的预约批次，请选择其他月份的预约进行审批。`)
      }
      
      // 构建审批数据，包含分配的探访日期
      const finalApprovalData = {
        ...approvalData,
        visitDate: finalVisitDate
      }
      
      // 准备传递给mutation的数据，当targetMonth存在且与原始月份不同时，包含month字段
      const updateData = {
        approvalInfo: finalApprovalData,
        visitDate: finalVisitDate // 更新预约的探访日期
      }
      
      // 如果使用了不同的月份，则更新month字段
      if (targetMonth && targetMonth !== appointment.month) {
        updateData.month = targetMonth
      }
      
      commit('UPDATE_APPOINTMENT_STATUS', {
        id,
        status: 'approved',
        data: updateData
      })
    },
    // 拒绝预约
    rejectAppointment({ commit }, { id, reason }) {
      commit('UPDATE_APPOINTMENT_STATUS', {
        id,
        status: 'rejected',
        data: { rejectionReason: reason }
      })
    },
    // 标记完成
    completeAppointment({ commit }, { id, notes }) {
      commit('UPDATE_APPOINTMENT_STATUS', {
        id,
        status: 'completed',
        data: { completionNotes: notes }
      })
    },
    // 删除预约
    deleteAppointment({ commit }, id) {
      commit('DELETE_APPOINTMENT', id)
    },
    // 管理员登录
    async adminLogin({ commit }, credentials) {
      try {
        // 登录验证已在组件中完成，这里直接获取登录状态
        const status = getLoginStatus()
        
        // 确保正确提交登录状态
        commit('SET_ADMIN_LOGIN', {
          isLoggedIn: status.loggedIn,
          user: status.user
        })
        
        return status.loggedIn
      } catch (error) {
        console.error('Login error:', error)
        // 出错时重置登录状态
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
        // 使用auth工具进行登出
        logoutAdmin()
        commit('SET_ADMIN_LOGIN', {
          isLoggedIn: false,
          user: null
        })
      } catch (error) {
        console.error('Logout error:', error)
      }
    },
    // 初始化登录状态
    async initializeLoginStatus({ commit }) {
      commit('INIT_LOGIN_STATUS')
    },
    // 用户登录（基于微信wxid）
    async userLogin({ commit }, wxid) {
      try {
        // 实际项目中应该调用微信API获取wxid并验证
        // 这里简化处理，直接使用传入的wxid
        commit('SET_USER_WXID', wxid)
        return { success: true }
      } catch (error) {
        console.error('用户登录失败:', error)
        throw error
      }
    },
    // 用户登出
    async userLogout({ commit }) {
      try {
        commit('CLEAR_USER_WXID')
      } catch (error) {
        console.error('用户登出失败:', error)
        throw error
      }
    }
  },
  modules: {}
})