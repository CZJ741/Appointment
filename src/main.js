import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import store from './store'

const app = createApp(App)

app.use(router)
app.use(store)

// 应用现在会保留localStorage中的预约数据，确保刷新页面后数据不会丢失

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
