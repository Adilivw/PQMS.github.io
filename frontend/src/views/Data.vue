<template>
  <div class="data-management">
    <!-- 查询条件 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="queryForm" class="query-form">
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="queryForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="车身区域">
          <el-select v-model="queryForm.bodyArea" placeholder="请选择">
            <el-option
              v-for="item in bodyAreaOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery">查询</el-button>
          <el-button @click="handleExport">导出</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 数据表格 -->
    <el-card class="table-card">
      <el-table
        :data="tableData"
        border
        style="width: 100%"
        height="500">
        <el-table-column
          type="index"
          width="50">
        </el-table-column>
        <el-table-column
          prop="timestamp"
          label="时间"
          width="180">
        </el-table-column>
        <el-table-column
          prop="bodyArea"
          label="车身区域"
          width="120">
        </el-table-column>
        <el-table-column
          prop="thickness"
          label="膜厚(μm)"
          width="100">
        </el-table-column>
        <el-table-column
          prop="doi"
          label="DOI"
          width="100">
        </el-table-column>
        <el-table-column
          prop="gloss"
          label="光泽度"
          width="100">
        </el-table-column>
        <el-table-column
          prop="temperature"
          label="温度(℃)"
          width="100">
        </el-table-column>
        <el-table-column
          prop="humidity"
          label="湿度(%)"
          width="100">
        </el-table-column>
        <el-table-column
          prop="viscosity"
          label="粘度(cp)"
          width="100">
        </el-table-column>
        <el-table-column
          label="操作"
          width="150">
          <template slot-scope="scope">
            <el-button
              size="mini"
              @click="handleDetail(scope.row)">详情</el-button>
            <el-button
              size="mini"
              type="danger"
              @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total">
        </el-pagination>
      </div>
    </el-card>

    <!-- 详情对话框 -->
    <el-dialog title="数据详情" :visible.sync="dialogVisible" width="70%">
      <el-descriptions :column="3" border>
        <el-descriptions-item label="时间">{{detailData.timestamp}}</el-descriptions-item>
        <el-descriptions-item label="车身区域">{{detailData.bodyArea}}</el-descriptions-item>
        <el-descriptions-item label="膜厚">{{detailData.thickness}} μm</el-descriptions-item>
        <el-descriptions-item label="DOI">{{detailData.doi}}</el-descriptions-item>
        <el-descriptions-item label="光泽度">{{detailData.gloss}}</el-descriptions-item>
        <el-descriptions-item label="色差">{{detailData.colorDiff}}</el-descriptions-item>
        <el-descriptions-item label="温度">{{detailData.temperature}} ℃</el-descriptions-item>
        <el-descriptions-item label="湿度">{{detailData.humidity}} %</el-descriptions-item>
        <el-descriptions-item label="粘度">{{detailData.viscosity}} cp</el-descriptions-item>
      </el-descriptions>
      
      <div class="detail-charts" v-if="dialogVisible">
        <div class="detail-chart" ref="trendChart"></div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'Data',
  data() {
    return {
      queryForm: {
        dateRange: [],
        bodyArea: ''
      },
      bodyAreaOptions: [
        { label: '垂直面', value: 'vertical' },
        { label: '水平面', value: 'horizontal' },
        { label: '凹面', value: 'concave' },
        { label: '凸面', value: 'convex' }
      ],
      tableData: [],
      currentPage: 1,
      pageSize: 20,
      total: 0,
      dialogVisible: false,
      detailData: {},
      trendChart: null
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      // 模拟数据
      this.tableData = Array.from({ length: 20 }, (_, index) => ({
        id: index + 1,
        timestamp: new Date().toLocaleString(),
        bodyArea: this.bodyAreaOptions[Math.floor(Math.random() * 4)].label,
        thickness: (25 + Math.random() * 2).toFixed(2),
        doi: (85 + Math.random() * 5).toFixed(2),
        gloss: (90 + Math.random() * 3).toFixed(2),
        temperature: (25 + Math.random() * 5).toFixed(1),
        humidity: (60 + Math.random() * 10).toFixed(1),
        viscosity: (18 + Math.random() * 4).toFixed(1)
      }))
      this.total = 100
    },
    handleQuery() {
      this.fetchData()
    },
    handleExport() {
      // 导出逻辑
    },
    handleDetail(row) {
      this.detailData = row
      this.dialogVisible = true
      this.$nextTick(() => {
        this.initTrendChart()
      })
    },
    handleDelete(row) {
      this.$confirm('确认删除该条数据?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 删除逻辑
        this.$message.success('删除成功')
      })
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.fetchData()
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.fetchData()
    },
    initTrendChart() {
      if (!this.trendChart) {
        this.trendChart = echarts.init(this.$refs.trendChart)
      }
      
      // 趋势图配置
      this.trendChart.setOption({
        title: { text: '历史趋势' },
        tooltip: { trigger: 'axis' },
        legend: { data: ['膜厚', 'DOI', '光泽度'] },
        xAxis: {
          type: 'category',
          data: Array.from({length: 24}, (_, i) => `${i}:00`)
        },
        yAxis: { type: 'value' },
        series: [
          {
            name: '膜厚',
            type: 'line',
            data: Array.from({length: 24}, () => (25 + Math.random() * 2).toFixed(1))
          },
          {
            name: 'DOI',
            type: 'line',
            data: Array.from({length: 24}, () => (85 + Math.random() * 5).toFixed(1))
          },
          {
            name: '光泽度',
            type: 'line',
            data: Array.from({length: 24}, () => (90 + Math.random() * 3).toFixed(1))
          }
        ]
      })
    }
  }
}
</script>

<style scoped>
.data-management {
  padding: 20px;
}

.filter-card {
  margin-bottom: 20px;
}

.table-card {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.detail-charts {
  margin-top: 20px;
}

.detail-chart {
  height: 300px;
  margin-top: 20px;
}
</style> 