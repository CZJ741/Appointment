// 管理员身份验证工具

// 模拟的管理员用户数据
const MOCK_ADMIN_USER = {
  username: 'admin',
  password: 'password123', // 实际应用中应该使用加密密码
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

// 验证管理员登录
const validateAdminLogin = (username, password, captcha) => {
  // 验证验证码
  if (!validateCaptcha(captcha)) {
    return {
      success: false,
      message: '验证码错误'
    }
  }

  // 验证用户名和密码
  if (username === MOCK_ADMIN_USER.username && password === MOCK_ADMIN_USER.password) {
    // 生成模拟token（实际应用中应该由后端生成）
    const token = `mock_token_${Date.now()}`
    
    // 存储登录状态
    localStorage.setItem('admin_token', token)
    localStorage.setItem('admin_user', JSON.stringify({
      username: MOCK_ADMIN_USER.username,
      name: MOCK_ADMIN_USER.name,
      role: MOCK_ADMIN_USER.role
    }))
    
    return {
      success: true,
      token,
      user: {
        username: MOCK_ADMIN_USER.username,
        name: MOCK_ADMIN_USER.name,
        role: MOCK_ADMIN_USER.role
      }
    }
  }
  
  return {
    success: false,
    message: '用户名或密码错误'
  }
}

// 检查是否已登录
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
  const token = localStorage.getItem('admin_token')
  if (!token) {
    return { loggedIn: false }
  }
  
  const isValid = validateToken(token)
  if (!isValid) {
    // token过期，清除登录状态
    logoutAdmin()
    return { loggedIn: false }
  }
  
  const user = getCurrentAdmin()
  return {
    loggedIn: true,
    user
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