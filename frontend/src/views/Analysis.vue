<template>
  <div class="analysis-container">
    <!-- AI预测模块 -->
    <el-row :gutter="20">
      <el-col :span="8">
        <div class="ai-prediction-panel">
          <div class="panel-header">
            <h3>AI智能预测</h3>
            <el-tag type="success">AI模型已就绪</el-tag>
          </div>
          <div class="prediction-form">
            <el-form :model="predictionForm" label-width="100px">
              <el-form-item label="温度(℃)">
                <el-slider v-model="predictionForm.temperature" :min="15" :max="35" :step="0.1" show-input></el-slider>
              </el-form-item>
              <el-form-item label="湿度(%)">
                <el-slider v-model="predictionForm.humidity" :min="30" :max="80" :step="1" show-input></el-slider>
              </el-form-item>
              <el-form-item label="粘度(cp)">
                <el-slider v-model="predictionForm.viscosity" :min="10" :max="30" :step="0.1" show-input></el-slider>
              </el-form-item>
              <el-button type="primary" class="predict-btn" @click="predict">
                <i class="el-icon-cpu"></i> 开始预测
              </el-button>
            </el-form>
          </div>
          <div v-if="predictionResult" class="prediction-result">
            <div class="result-title">预测结果</div>
            <div class="result-item">
              <div class="item-label">预测膜厚</div>
              <div class="item-value">{{predictionResult.thickness}} μm</div>
              <el-progress :percentage="predictionResult.confidence" :color="confidenceColor"></el-progress>
            </div>
            <div class="result-tips">
              <i class="el-icon-info"></i>
              建议调整参数以获得更好的涂装效果
            </div>
          </div>
        </div>
      </el-col>
      
      <el-col :span="16">
        <div class="correlation-panel">
          <div class="panel-header">
            <h3>参数相关性分析</h3>
            <div class="panel-tools">
              <el-radio-group v-model="analysisType" size="small">
                <el-radio-button label="correlation">相关性</el-radio-button>
                <el-radio-button label="trend">趋势分析</el-radio-button>
              </el-radio-group>
            </div>
          </div>
          <div class="correlation-chart" ref="correlationChart"></div>
        </div>
      </el-col>
    </el-row>

    <!-- 工艺优化建议 -->
    <div class="optimization-panel">
      <div class="panel-header">
        <h3>智能工艺优化建议</h3>
        <el-button type="text" @click="refreshSuggestions">
          <i class="el-icon-refresh"></i> 刷新建议
        </el-button>
      </div>
      <div class="suggestions-container">
        <el-row :gutter="20">
          <el-col :span="8" v-for="(suggestion, index) in suggestions" :key="index">
            <div class="suggestion-card" :class="suggestion.type">
              <div class="suggestion-icon">
                <i :class="suggestion.icon"></i>
              </div>
              <div class="suggestion-content">
                <div class="suggestion-title">{{suggestion.title}}</div>
                <div class="suggestion-desc">{{suggestion.description}}</div>
                <div class="suggestion-impact">
                  预期提升: <span>{{suggestion.impact}}</span>
                </div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>

    <!-- 特征重要性分析 -->
    <div class="feature-importance-panel">
      <div class="panel-header">
        <h3>特征重要性分析</h3>
      </div>
      <div class="importance-chart" ref="importanceChart"></div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { mapActions } from 'vuex'

export default {
  name: 'Analysis',
  data() {
    return {
      analysisType: 'correlation',
      predictionForm: {
        temperature: 25,
        humidity: 60,
        viscosity: 18
      },
      predictionResult: null,
      suggestions: [
        {
          title: '温度优化',
          description: '建议将喷涂温度调整至23.5℃，可提高漆膜均匀性',
          impact: '+15%',
          type: 'primary',
          icon: 'el-icon-temperature'
        },
        {
          title: '湿度控制',
          description: '当前湿度偏高，建议降低至55%以下',
          impact: '+8%',
          type: 'warning',
          icon: 'el-icon-umbrella'
        },
        {
          title: '粘度调整',
          description: '适当提高粘度可改善流平性能',
          impact: '+12%',
          type: 'success',
          icon: 'el-icon-water-cup'
        }
      ]
    }
  },
  computed: {
    confidenceColor() {
      return (percentage) => {
        if (percentage > 80) return '#67C23A'
        if (percentage > 60) return '#E6A23C'
        return '#F56C6C'
      }
    }
  },
  mounted() {
    this.initCharts()
  },
  methods: {
    ...mapActions(['predictQuality']),
    
    initCharts() {
      this.initCorrelationChart()
      this.initImportanceChart()
    },
    
    initCorrelationChart() {
      const chart = echarts.init(this.$refs.correlationChart)
      // ... 相关性图表配置
    },
    
    initImportanceChart() {
      const chart = echarts.init(this.$refs.importanceChart)
      // ... 特征重要性图表配置
    },
    
    async predict() {
      try {
        const result = await this.predictQuality(this.predictionForm)
        this.predictionResult = result
      } catch (error) {
        this.$message.error('预测失败')
      }
    },
    
    refreshSuggestions() {
      // 刷新优化建议
    }
  }
}
</script>

<style lang="scss" scoped>
.analysis-container {
  padding: 20px;
  background: #f0f2f5;
  min-height: 100vh;
}

.ai-prediction-panel, .correlation-panel, .optimization-panel, .feature-importance-panel {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

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

.prediction-form {
  padding: 20px 0;
  
  .predict-btn {
    width: 100%;
    margin-top: 20px;
  }
}

.prediction-result {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #EBEEF5;
  
  .result-title {
    font-size: 16px;
    color: #303133;
    margin-bottom: 15px;
  }
  
  .result-item {
    margin-bottom: 15px;
    
    .item-label {
      font-size: 14px;
      color: #909399;
      margin-bottom: 5px;
    }
    
    .item-value {
      font-size: 24px;
      font-weight: bold;
      color: #409EFF;
      margin-bottom: 10px;
    }
  }
  
  .result-tips {
    font-size: 12px;
    color: #909399;
    padding: 10px;
    background: #f4f4f5;
    border-radius: 4px;
    
    i {
      margin-right: 5px;
    }
  }
}

.correlation-chart, .importance-chart {
  height: 400px;
}

.suggestions-container {
  .suggestion-card {
    background: #fff;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    display: flex;
    align-items: flex-start;
    transition: all 0.3s;
    
    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .suggestion-icon {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 15px;
      
      i {
        font-size: 20px;
        color: #fff;
      }
    }
    
    &.primary {
      border-left: 4px solid #409EFF;
      .suggestion-icon { background: #409EFF; }
    }
    
    &.warning {
      border-left: 4px solid #E6A23C;
      .suggestion-icon { background: #E6A23C; }
    }
    
    &.success {
      border-left: 4px solid #67C23A;
      .suggestion-icon { background: #67C23A; }
    }
    
    .suggestion-content {
      flex: 1;
      
      .suggestion-title {
        font-size: 16px;
        font-weight: bold;
        color: #303133;
        margin-bottom: 8px;
      }
      
      .suggestion-desc {
        font-size: 14px;
        color: #606266;
        margin-bottom: 8px;
      }
      
      .suggestion-impact {
        font-size: 12px;
        color: #909399;
        
        span {
          color: #67C23A;
          font-weight: bold;
        }
      }
    }
  }
}
</style> 