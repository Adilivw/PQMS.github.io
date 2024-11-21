import axios from 'axios'
import { Message } from 'element-ui'
import router from '@/router'

const baseURL = process.env.NODE_ENV === 'production'
  ? process.env.VUE_APP_BASE_API
  : 'http://localhost:8000/api'

const api = axios.create({
  baseURL,
  timeout: 5000
})

// 添加请求拦截器
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

// 添加响应拦截器
api.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          localStorage.removeItem('token')
          router.push('/login')
          Message.error('登录已过期，请重新登录')
          break
        case 403:
          Message.error('没有权限访问')
          break
        case 500:
          Message.error('服务器错误')
          break
        default:
          Message.error(error.response.data.message || '请求失败')
      }
    } else {
      Message.error('网络连接失败')
    }
    return Promise.reject(error)
  }
)

export default {
  // 数据管理
  getCoatingData(params) {
    return api.get('/coating/data', { params })
  },
  
  createCoatingData(data) {
    return api.post('/coating/data', data)
  },
  
  // SPC分析
  getSPCAnalysis(params) {
    return api.get('/spc/analysis', { params })
  },
  
  // 智能分析
  getCorrelationAnalysis() {
    return api.get('/analysis/correlation')
  },
  
  predictQuality(params) {
    return api.post('/analysis/predict', params)
  },
  
  // 实时监控
  getRealtimeData() {
    return api.get('/monitor/realtime')
  }
} 