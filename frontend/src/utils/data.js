export function formatDateTime(date) {
  const d = new Date(date)
  const pad = (n) => n < 10 ? `0${n}` : n
  
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
}

export function calculateStatistics(data) {
  const values = data.map(d => parseFloat(d))
  const n = values.length
  
  // 计算平均值
  const mean = values.reduce((a, b) => a + b) / n
  
  // 计算标准差
  const std = Math.sqrt(
    values.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / (n - 1)
  )
  
  // 计算最大最小值
  const max = Math.max(...values)
  const min = Math.min(...values)
  
  return { mean, std, max, min }
}

export function isOutOfControl(value, ucl, lcl) {
  return value > ucl || value < lcl
}

export function generateRandomId() {
  return Math.random().toString(36).substr(2, 9)
} 