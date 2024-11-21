import { Message } from 'element-ui'

export function handleError(error) {
  console.error('Error:', error)
  
  let message = '操作失败'
  if (error.response) {
    // 服务器响应错误
    const status = error.response.status
    const data = error.response.data
    
    switch (status) {
      case 400:
        message = data.message || '请求参数错误'
        break
      case 401:
        message = '未授权，请重新登录'
        // 可以在这里处理登录过期
        break
      case 403:
        message = '拒绝访问'
        break
      case 404:
        message = '请求的资源不存在'
        break
      case 500:
        message = '服务器错误'
        break
      default:
        message = data.message || '未知错误'
    }
  } else if (error.request) {
    // 请求未收到响应
    message = '网络连接失败'
  }
  
  Message.error(message)
  return Promise.reject(error)
} 