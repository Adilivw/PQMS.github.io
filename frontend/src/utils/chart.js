import * as echarts from 'echarts'

export const chartTheme = {
  color: ['#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399'],
  backgroundColor: '#ffffff',
  textStyle: {},
  title: {
    textStyle: {
      color: '#303133'
    },
    subtextStyle: {
      color: '#909399'
    }
  },
  line: {
    itemStyle: {
      borderWidth: 1
    },
    lineStyle: {
      width: 2
    },
    symbolSize: 4,
    symbol: 'circle',
    smooth: false
  },
  radar: {
    itemStyle: {
      borderWidth: 1
    },
    lineStyle: {
      width: 2
    },
    symbolSize: 4,
    symbol: 'circle',
    smooth: false
  }
}

export function initChart(el, option) {
  const chart = echarts.init(el)
  chart.setOption(option)
  
  window.addEventListener('resize', () => {
    chart.resize()
  })
  
  return chart
}

export function getSPCChartOption(data, limits) {
  return {
    title: { text: 'SPC控制图' },
    tooltip: { trigger: 'axis' },
    legend: {
      data: ['测量值', 'UCL', 'CL', 'LCL']
    },
    xAxis: {
      type: 'category',
      data: data.map((_, index) => index + 1)
    },
    yAxis: { type: 'value' },
    series: [
      {
        name: '测量值',
        type: 'line',
        data: data,
        markLine: {
          data: [
            { name: 'UCL', yAxis: limits.ucl },
            { name: 'CL', yAxis: limits.cl },
            { name: 'LCL', yAxis: limits.lcl }
          ]
        }
      }
    ]
  }
}

export function getCorrelationChartOption(data) {
  return {
    tooltip: {
      position: 'top',
      formatter: (params) => {
        return `相关系数: ${params.data[2].toFixed(2)}`
      }
    },
    grid: {
      top: '10%',
      bottom: '15%'
    },
    xAxis: {
      type: 'category',
      data: data.x_labels,
      splitArea: { show: true }
    },
    yAxis: {
      type: 'category',
      data: data.y_labels,
      splitArea: { show: true }
    },
    visualMap: {
      min: -1,
      max: 1,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '5%',
      inRange: {
        color: ['#F56C6C', '#FFFFFF', '#67C23A']
      }
    },
    series: [{
      name: '相关性系数',
      type: 'heatmap',
      data: data.correlation_data,
      label: {
        show: true,
        formatter: (params) => params.data[2].toFixed(2)
      }
    }]
  }
} 