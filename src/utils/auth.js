// 管理员身份验证工具

// 模拟的管理员用户数据
const MOCK_ADMIN_USER = {
  username: 'admin',
  password: 'admin123', // 实际应用中应该使用加密密码
  name: '系统管理员',
  role: 'admin'
}

// 生成验证码
const generateCaptcha = () => {
  const chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
  let captcha = ''
  for (let i = 0; i < 4; i++) {
    captcha += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  // 存储验证码到sessionStorage
  sessionStorage.setItem('captcha', captcha)
  return captcha
}

// 验证验证码
const validateCaptcha = (input) => {
  const storedCaptcha = sessionStorage.getItem('captcha')
  return storedCaptcha && input.toUpperCase() === storedCaptcha.toUpperCase()
}

// 管理员登录函数 - 调用后端API进行验证
const validateAdminLogin = async (username, password, captcha) => {
  try {
    // 调用后端用户登录接口
    const response = await fetch('http://apb.vgit.cn/api/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password })
    });
    
    const data = await response.json();
    
    if (response.ok && data.is_staff) {
      // 保存登录状态
      localStorage.setItem('admin_token', data.token)
      localStorage.setItem('admin_user', JSON.stringify({
        username: data.username,
        full_name: data.full_name,
        is_staff: data.is_staff
      }))
      
      return { 
        success: true, 
        token: data.token, 
        user: {
          username: data.username,
          full_name: data.full_name,
          is_staff: data.is_staff
        } 
      }
    } else if (response.ok && !data.is_staff) {
      return { 
        success: false, 
        message: '该用户不是管理员' 
      }
    } else {
      return { 
        success: false, 
        message: data.error || '用户名或密码错误' 
      }
    }
  } catch (error) {
    console.error('登录错误:', error)
    return { 
      success: false, 
      message: '登录过程中发生错误' 
    }
  }
}

// 检查用户是否已登录
const isAdminLoggedIn = () => {
  const token = localStorage.getItem('admin_token')
  return !!token
}

// 获取当前用户信息
const getCurrentAdmin = () => {
  const userStr = localStorage.getItem('admin_user')
  return userStr ? JSON.parse(userStr) : null
}

// 登出
const logoutAdmin = () => {
  localStorage.removeItem('admin_token')
  localStorage.removeItem('admin_user')
  sessionStorage.removeItem('captcha')
}

// 验证token有效性（模拟）
const validateToken = (token) => {
  // 简单的时间验证，token有效期24小时
  const tokenParts = token.split('_')
  if (tokenParts.length >= 3) {
    const tokenTime = parseInt(tokenParts[2])
    const now = Date.now()
    const tokenAge = now - tokenTime
    return tokenAge < 24 * 60 * 60 * 1000 // 24小时
  }
  return false
}

// 获取登录状态
const getLoginStatus = () => {
  try {
    const token = localStorage.getItem('admin_token')
    if (!token) {
      return { loggedIn: false, user: null }
    }
    
    // 从localStorage获取用户信息
    // 注意：在真实项目中，应该定期向后端验证token的有效性
    const user = getCurrentAdmin()
    return { loggedIn: !!user, user: user }
  } catch (error) {
    console.error('获取登录状态失败:', error)
    return { loggedIn: false, user: null }
  }
}

export {
  generateCaptcha,
  validateCaptcha,
  validateAdminLogin,
  isAdminLoggedIn,
  getCurrentAdmin,
  logoutAdmin,
  validateToken,
  getLoginStatus
}