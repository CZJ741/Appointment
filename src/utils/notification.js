import { createApp, h } from 'vue'
import Notification from '../components/Notification.vue'

// 通知管理器
class NotificationManager {
  constructor() {
    this.notifications = []
    this.container = null
    this.setupContainer()
  }

  // 设置容器
  setupContainer() {
    this.container = document.createElement('div')
    this.container.className = 'notification-container fixed top-0 right-0 z-50 p-4 flex flex-col gap-4'
    document.body.appendChild(this.container)
  }

  // 创建通知
  createNotification(options) {
    const {
      type = 'info',
      title,
      message = '',
      duration = 5000,
      showProgress = true
    } = options

    // 生成唯一ID
    const id = Date.now() + Math.floor(Math.random() * 1000)

    // 创建应用实例
    const that = this;
    const app = createApp({
      render() {
        return h(Notification, {
          type,
          title,
          message,
          duration,
          showProgress,
          onClose: () => that.removeNotification(id)
        })
      }
    })

    // 创建挂载点
    const mountPoint = document.createElement('div')
    this.container.appendChild(mountPoint)

    // 挂载组件
    app.mount(mountPoint)

    // 存储通知信息
    const notification = {
      id,
      app,
      mountPoint
    }

    this.notifications.push(notification)
    
    // 限制最大通知数量
    this.limitNotifications()

    return id
  }

  // 限制通知数量
  limitNotifications(max = 5) {
    while (this.notifications.length > max) {
      const oldest = this.notifications.shift()
      this.unmountNotification(oldest)
    }
  }

  // 移除通知
  removeNotification(id) {
    const index = this.notifications.findIndex(n => n.id === id)
    if (index !== -1) {
      const notification = this.notifications.splice(index, 1)[0]
      setTimeout(() => {
        this.unmountNotification(notification)
      }, 300) // 等待动画结束
    }
  }

  // 卸载通知组件
  unmountNotification(notification) {
    notification.app.unmount()
    if (notification.mountPoint.parentNode) {
      notification.mountPoint.parentNode.removeChild(notification.mountPoint)
    }
  }

  // 关闭所有通知
  closeAll() {
    this.notifications.forEach(notification => {
      this.unmountNotification(notification)
    })
    this.notifications = []
  }

  // 成功通知
  success(options) {
    if (typeof options === 'string') {
      return this.createNotification({
        type: 'success',
        title: options
      })
    }
    return this.createNotification({
      type: 'success',
      ...options
    })
  }

  // 错误通知
  error(options) {
    if (typeof options === 'string') {
      return this.createNotification({
        type: 'error',
        title: options
      })
    }
    return this.createNotification({
      type: 'error',
      ...options
    })
  }

  // 警告通知
  warning(options) {
    if (typeof options === 'string') {
      return this.createNotification({
        type: 'warning',
        title: options
      })
    }
    return this.createNotification({
      type: 'warning',
      ...options
    })
  }

  // 信息通知
  info(options) {
    if (typeof options === 'string') {
      return this.createNotification({
        type: 'info',
        title: options
      })
    }
    return this.createNotification({
      type: 'info',
      ...options
    })
  }
}

// 导出单例实例
export default new NotificationManager()