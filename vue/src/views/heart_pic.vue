<template>
  <div>
    <!-- 开始/停止模拟按钮 -->
    <el-button
        type="primary"
        @click="toggleAutoRefresh"
        style="margin-top: 20px; margin-bottom: 20px;"
    >
      {{ isAutoRefreshing ? '停止模拟' : '开始模拟' }}
    </el-button>

    <!-- 心率折线图 + 心率监测组件 -->
    <div style="width: 100%; display: flex; justify-content: space-around; flex-wrap: wrap;">
      <!-- 心率折线图 -->
      <div id="main-line" style="width: 600px; height: 400px;"></div>

      <!-- 心率监测组件 -->
      <div style="width: 600px; height: 400px; display: flex; align-items: center; justify-content: center;">
        <el-card style="width: 520px; height: 300px">
          <HeartRateMonitor :rate="currentHeartRate" />
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import * as echarts from 'echarts'
import HeartRateMonitor from './HeartRateMonitor.vue'

// 自动刷新控制
const isAutoRefreshing = ref(false)
const currentHeartRate = ref(0)

// ECharts 配置
let myChartLine = null
const optionLine = ref({
  title: { text: '心率数据折线图' },
  xAxis: { type: 'category', data: [] },
  yAxis: { type: 'value' },
  legend: { data: ['心率数据'] },
  series: [{ name: '心率数据', data: [], type: 'line' }]
})

const data = reactive({
  chartData: []
})

// 加载心率数据并更新图表
const loadHeartRateData = async () => {
  try {
    const response = await fetch('/result.json')
    if (!response.ok) throw new Error(`HTTP error: ${response.status}`)
    const jsonData = await response.json()
    const heartrate = jsonData.heartrate

    currentHeartRate.value = heartrate

    // 更新图表数据
    if (!data.chartData) data.chartData = []
    data.chartData.push(heartrate)

    const maxPoints = 20
    if (data.chartData.length > maxPoints) data.chartData.shift()

    const dataLength = data.chartData.length
    optionLine.value.xAxis.data = Array.from({ length: dataLength }, (_, i) => `点${i + 1}`)
    optionLine.value.series[0].data = data.chartData

    if (myChartLine) {
      myChartLine.setOption(optionLine.value)
    }
  } catch (error) {
    console.error('加载 result.json 失败:', error)
  }
}

// 初始化 ECharts
const initChart = () => {
  const chartDom = document.getElementById('main-line')
  if (chartDom) {
    myChartLine = echarts.init(chartDom)
    myChartLine.setOption(optionLine.value)
  }
}

// 切换自动刷新
const toggleAutoRefresh = () => {
  if (isAutoRefreshing.value) {
    clearInterval(window.heartRateRefreshTimerInner)
    window.heartRateRefreshTimerInner = null
    isAutoRefreshing.value = false
    console.log('⏹️ 自动刷新已停止')
  } else {
    loadHeartRateData() // 立即加载一次
    window.heartRateRefreshTimerInner = setInterval(loadHeartRateData, 2500)
    isAutoRefreshing.value = true
    console.log('▶️ 自动刷新已开启：每2.5秒更新')
  }
}

// 组件挂载
onMounted(() => {
  initChart()
})
</script>

<style scoped>
/* 可根据需要添加响应式样式 */
@media (max-width: 1250px) {
  #main-line,
  .el-card {
    width: 95% !important;
    margin-bottom: 20px;
  }
}
</style>