<template>
  <div class="dashboard-container">
    <!-- 顶部数据卡片 -->
    <div class="data-overview">
      <el-row :gutter="20">
        <el-col :span="6" v-for="(item, index) in overviewData" :key="index">
          <div class="data-card" :class="item.type">
            <div class="card-icon">
              <i :class="item.icon"></i>
            </div>
            <div class="card-info">
              <div class="card-title">{{item.title}}</div>
              <div class="card-value">{{item.value}}</div>
              <div class="card-trend">
                <span :class="item.trend > 0 ? 'up' : 'down'">
                  {{Math.abs(item.trend)}}%
                  <i :class="item.trend > 0 ? 'el-icon-top' : 'el-icon-bottom'"></i>
                </span>
                较上周
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 主要图表区域 -->
    <div class="chart-container">
      <el-row :gutter="20">
        <el-col :span="16">
          <div class="chart-panel">
            <div class="panel-header">
              <h3>实时生产监控</h3>
              <div class="panel-tools">
                <el-radio-group v-model="timeRange" size="small">
                  <el-radio-button label="today">今日</el-radio-button>
                  <el-radio-button label="week">本周</el-radio-button>
                  <el-radio-button label="month">本月</el-radio-button>
                </el-radio-group>
              </div>
            </div>
            <div class="chart" ref="productionChart"></div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="chart-panel">
            <div class="panel-header">
              <h3>质量分布</h3>
            </div>
            <div class="chart" ref="qualityChart"></div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 实时告警和工艺参数 -->
    <el-row :gutter="20">
      <el-col :span="12">
        <div class="alert-panel">
          <div class="panel-header">
            <h3>实时告警</h3>
            <el-tag type="danger">{{alerts.length}}个待处理</el-tag>
          </div>
          <div class="alert-list">
            <div v-for="alert in alerts" :key="alert.id" class="alert-item">
              <div class="alert-icon" :class="alert.level">
                <i class="el-icon-warning"></i>
              </div>
              <div class="alert-content">
                <div class="alert-title">{{alert.title}}</div>
                <div class="alert-time">{{alert.time}}</div>
              </div>
              <el-button size="mini" type="primary">处理</el-button>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="params-panel">
          <div class="panel-header">
            <h3>关键工艺参数</h3>
          </div>
          <div class="params-grid">
            <div v-for="param in parameters" :key="param.name" class="param-item">
              <div class="param-name">{{param.name}}</div>
              <div class="param-value" :class="param.status">
                {{param.value}}
                <small>{{param.unit}}</small>
              </div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { mapState, mapActions } from 'vuex'

export default {
  name: 'Dashboard',
  data() {
    return {
      timeRange: 'today',
      overviewData: [
        {
          title: '今日产量',
          value: '2,456',
          trend: 5.6,
          type: 'primary',
          icon: 'el-icon-s-data'
        },
        {
          title: '合格率',
          value: '98.5%',
          trend: 2.1,
          type: 'success',
          icon: 'el-icon-s-check'
        },
        {
          title: '能耗指数',
          value: '89.2',
          trend: -3.2,
          type: 'warning',
          icon: 'el-icon-lightning'
        },
        {
          title: '设备稼动率',
          value: '95.8%',
          trend: 1.8,
          type: 'info',
          icon: 'el-icon-cpu'
        }
      ],
      alerts: [
        {
          id: 1,
          title: '1号生产线温度异常',
          time: '10分钟前',
          level: 'critical'
        },
        {
          id: 2,
          title: '2号喷枪压力波动',
          time: '25分钟前',
          level: 'warning'
        }
      ],
      parameters: [
        { name: '喷涂温度', value: '25.6', unit: '℃', status: 'normal' },
        { name: '环境湿度', value: '65', unit: '%', status: 'warning' },
        { name: '涂料粘度', value: '18.2', unit: 'cp', status: 'normal' },
        { name: '风速', value: '0.3', unit: 'm/s', status: 'normal' }
      ]
    }
  },
  mounted() {
    this.initCharts()
    this.startRealTimeUpdate()
  },
  methods: {
    ...mapActions(['fetchRealtimeData']),
    
    initCharts() {
      // 生产监控图表
      const productionChart = echarts.init(this.$refs.productionChart)
      productionChart.setOption({
        // ... 生产监控图表配置
      })
      
      // 质量分布图表
      const qualityChart = echarts.init(this.$refs.qualityChart)
      qualityChart.setOption({
        // ... 质量分布图表配置
      })
    },
    
    startRealTimeUpdate() {
      setInterval(() => {
        this.fetchRealtimeData()
      }, 5000)
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard-container {
  padding: 20px;
  background: #f0f2f5;
  min-height: 100vh;
}

.data-overview {
  margin-bottom: 20px;
  
  .data-card {
    background: #fff;
    border-radius: 8px;
    padding: 20px;
    display: flex;
    align-items: center;
    transition: all 0.3s;
    cursor: pointer;
    
    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .card-icon {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 15px;
      
      i {
        font-size: 30px;
        color: #fff;
      }
    }
    
    &.primary .card-icon { background: #409EFF; }
    &.success .card-icon { background: #67C23A; }
    &.warning .card-icon { background: #E6A23C; }
    &.info .card-icon { background: #909399; }
    
    .card-info {
      flex: 1;
      
      .card-title {
        font-size: 14px;
        color: #909399;
        margin-bottom: 5px;
      }
      
      .card-value {
        font-size: 24px;
        font-weight: bold;
        color: #303133;
      }
      
      .card-trend {
        font-size: 12px;
        color: #909399;
        margin-top: 5px;
        
        .up { color: #67C23A; }
        .down { color: #F56C6C; }
      }
    }
  }
}

.chart-panel {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  
  .panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    h3 {
      margin: 0;
      font-size: 18px;
      color: #303133;
    }
  }
  
  .chart {
    height: 350px;
  }
}

.alert-panel, .params-panel {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  height: 400px;
  
  .alert-list {
    .alert-item {
      display: flex;
      align-items: center;
      padding: 15px 0;
      border-bottom: 1px solid #EBEEF5;
      
      .alert-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 15px;
        
        &.critical { background: #F56C6C; }
        &.warning { background: #E6A23C; }
        
        i {
          color: #fff;
          font-size: 20px;
        }
      }
    }
  }
  
  .params-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    padding: 20px 0;
    
    .param-item {
      text-align: center;
      
      .param-name {
        font-size: 14px;
        color: #909399;
        margin-bottom: 10px;
      }
      
      .param-value {
        font-size: 24px;
        font-weight: bold;
        
        &.normal { color: #67C23A; }
        &.warning { color: #E6A23C; }
        &.danger { color: #F56C6C; }
        
        small {
          font-size: 14px;
          margin-left: 5px;
        }
      }
    }
  }
}
</style> 