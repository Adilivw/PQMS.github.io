<template>
  <div class="spc-container">
    <!-- 参数选择和控制面板 -->
    <div class="control-panel">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="param-select">
            <div class="panel-title">监控参数</div>
            <el-select v-model="selectedParam" style="width: 100%">
              <el-option
                v-for="item in paramOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value">
                <span class="param-icon"><i :class="item.icon"></i></span>
                {{item.label}}
              </el-option>
            </el-select>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="time-range">
            <div class="panel-title">时间范围</div>
            <el-date-picker
              v-model="dateRange"
              type="datetimerange"
              range-separator="至"
              start-placeholder="开始时间"
              end-placeholder="结束时间"
              :picker-options="pickerOptions"
              style="width: 100%">
            </el-date-picker>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="control-buttons">
            <div class="panel-title">操作</div>
            <el-button-group>
              <el-button type="primary" @click="refreshData">
                <i class="el-icon-refresh"></i> 刷新
              </el-button>
              <el-button type="success" @click="exportData">
                <i class="el-icon-download"></i> 导出
              </el-button>
            </el-button-group>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- SPC图表区域 -->
    <div class="chart-container">
      <el-row :gutter="20">
        <el-col :span="24">
          <div class="chart-panel">
            <div class="panel-header">
              <h3>X-bar控制图</h3>
              <el-tag v-if="processStatus" :type="processStatus.type">
                {{processStatus.text}}
              </el-tag>
            </div>
            <div class="chart" ref="xbarChart"></div>
            <div class="chart-footer">
              <div class="stat-item" v-for="(stat, index) in xbarStats" :key="index">
                <div class="stat-label">{{stat.label}}</div>
                <div class="stat-value" :class="stat.status">{{stat.value}}</div>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <div class="chart-panel">
            <div class="panel-header">
              <h3>R控制图</h3>
            </div>
            <div class="chart" ref="rChart"></div>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="chart-panel">
            <div class="panel-header">
              <h3>过程能力分析</h3>
            </div>
            <div class="chart" ref="capabilityChart"></div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 异常点分析 -->
    <div class="analysis-panel">
      <div class="panel-header">
        <h3>异常点分析</h3>
        <el-badge :value="outOfControlPoints.length" class="warning-badge">
          <el-button type="text">异常点清单</el-button>
        </el-badge>
      </div>
      <el-table :data="outOfControlPoints" height="250" border>
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="time" label="时间" width="180"></el-table-column>
        <el-table-column prop="value" label="测量值"></el-table-column>
        <el-table-column prop="type" label="异常类型">
          <template slot-scope="scope">
            <el-tag :type="scope.row.type === 'UCL' ? 'danger' : 'warning'">
              {{scope.row.type}}越限
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="deviation" label="偏差值"></el-table-column>
        <el-table-column label="操作" width="120">
          <template slot-scope="scope">
            <el-button type="text" @click="handleAnalyze(scope.row)">分析</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { mapActions } from 'vuex'

export default {
  name: 'SPC',
  data() {
    return {
      selectedParam: 'thickness',
      dateRange: [],
      pickerOptions: {
        shortcuts: [{
          text: '最近一天',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近一周',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
            picker.$emit('pick', [start, end])
          }
        }]
      },
      paramOptions: [
        { label: '膜厚', value: 'thickness', icon: 'el-icon-tickets' },
        { label: 'DOI', value: 'doi', icon: 'el-icon-view' },
        { label: '光泽度', value: 'gloss', icon: 'el-icon-sunny' },
        { label: '色差', value: 'colorDiff', icon: 'el-icon-picture' }
      ],
      processStatus: {
        type: 'success',
        text: '过程稳定'
      },
      xbarStats: [
        { label: 'Cp', value: '1.33', status: 'good' },
        { label: 'Cpk', value: '1.28', status: 'good' },
        { label: 'Pp', value: '1.31', status: 'good' },
        { label: 'Ppk', value: '1.26', status: 'warning' }
      ],
      outOfControlPoints: [
        {
          time: '2024-01-20 10:30:00',
          value: '29.5',
          type: 'UCL',
          deviation: '+1.5'
        },
        {
          time: '2024-01-20 11:15:00',
          value: '21.8',
          type: 'LCL',
          deviation: '-0.2'
        }
      ]
    }
  },
  mounted() {
    this.initCharts()
  },
  methods: {
    ...mapActions(['fetchSPCData']),
    
    initCharts() {
      this.initXbarChart()
      this.initRChart()
      this.initCapabilityChart()
    },
    
    initXbarChart() {
      const chart = echarts.init(this.$refs.xbarChart)
      chart.setOption({
        // ... X-bar图表配置
      })
    },
    
    initRChart() {
      const chart = echarts.init(this.$refs.rChart)
      chart.setOption({
        // ... R图表配置
      })
    },
    
    initCapabilityChart() {
      const chart = echarts.init(this.$refs.capabilityChart)
      chart.setOption({
        // ... 过程能力分析图表配置
      })
    },
    
    refreshData() {
      // 刷新数据
    },
    
    exportData() {
      // 导出数据
    },
    
    handleAnalyze(point) {
      // 分析异常点
    }
  }
}
</script>

<style lang="scss" scoped>
.spc-container {
  padding: 20px;
  background: #f0f2f5;
  min-height: 100vh;
}

.control-panel {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  
  .panel-title {
    font-size: 14px;
    color: #606266;
    margin-bottom: 10px;
  }
  
  .param-icon {
    margin-right: 8px;
    
    i {
      font-size: 16px;
    }
  }
}

.chart-panel {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  
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
    height: 300px;
  }
  
  .chart-footer {
    display: flex;
    justify-content: space-around;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #EBEEF5;
    
    .stat-item {
      text-align: center;
      
      .stat-label {
        font-size: 14px;
        color: #909399;
        margin-bottom: 5px;
      }
      
      .stat-value {
        font-size: 24px;
        font-weight: bold;
        
        &.good { color: #67C23A; }
        &.warning { color: #E6A23C; }
        &.danger { color: #F56C6C; }
      }
    }
  }
}

.analysis-panel {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  
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
  
  .warning-badge {
    margin-top: 10px;
  }
}
</style> 