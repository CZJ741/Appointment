import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import store from './store'

const app = createApp(App)

app.use(router)
app.use(store)

// 应用使用后端API进行数据存储和获取

// 初始化应用
async function initializeApp() {
  try {
    // 初始化登录状态
    await store.dispatch('initializeLoginStatus')
    
    // 初始化预约数据
    await store.dispatch('initializeData')
  } catch (error) {
    console.error('初始化应用失败:', error)
  }
}

// 启动初始化
initializeApp()

app.mount('#app')
