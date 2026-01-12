import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  },
  server: {
    proxy: {
      // 将所有以/api开头的请求转发到后端8000端口
      '/api': {
        target: 'http://apb.vgit.cn',
        changeOrigin: true,
        rewrite: (path) => path
      }
    }
  }
})
