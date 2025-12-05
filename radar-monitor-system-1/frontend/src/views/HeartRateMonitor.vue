<template>
  <div class="heart-rate-monitor">
    <div class="monitor-header">
      <svg class="heart-icon" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12,21.35L10.55,20.03C5.4,15.36 2,12.27 2,8.5C2,5.41 4.42,3 7.5,3C9.24,3 10.91,3.81 12,5.08C13.09,3.81 14.76,3 16.5,3C19.58,3 22,5.41 22,8.5C22,12.27 18.6,15.36 13.45,20.03L12,21.35Z" />
      </svg>
      <span class="title-text">心率监测</span>
    </div>

    <div class="monitor-subtitle">实时心率数据</div>

    <div class="heart-rate-data">
      <div class="rate-display">
        <span class="rate-value" :style="{color: statusColor}">{{ rate }}</span>
        <span class="rate-unit">BPM</span>
      </div>

      <div class="status-indicator" :class="[statusClass, { 'abnormal-text': !isNormal }]" :style="{color: statusColor}">
        {{ statusText }}
      </div>
    </div>

    <div class="heart-rate-scale">
      <div class="scale-container">
        <div class="scale-fill" :style="{width: fillPercentage + '%', backgroundColor: statusColor}"></div>
      </div>

      <div class="scale-marks">
        <span v-for="mark in scaleMarks" :key="mark" class="scale-mark">{{ mark }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  rate: {
    type: Number,
    default: 0
  }
});

// 计算状态文本
const statusText = computed(() => {
  if (props.rate < 60) return '过缓';
  if (props.rate < 100) return '正常';
  return '过快';
});

// 计算状态颜色
const statusColor = computed(() => {
  if (props.rate < 60) return '#f5222d'; // 绿色 - 过缓
  if (props.rate < 100) return '#52c41a'; // 绿色 - 正常
  return '#f5222d'; // 红色 - 过快
});

// 计算状态类名
const statusClass = computed(() => {
  if (props.rate < 60) return 'status-slow';
  if (props.rate < 100) return 'status-normal';
  return 'status-fast';
});

// 计算是否为正常心率
const isNormal = computed(() => props.rate >= 60 && props.rate < 100);

// 计算刻度填充百分比
const fillPercentage = computed(() => {
  return ((props.rate - 60) / 60) * 100;
});


const scaleMarks = [60, 80, 100, 120];
</script>

<style scoped>
.heart-rate-monitor {
  width: 100%;
  max-width: 450px;
  background-color: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 16px;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

.monitor-header {
  background-color: #e6f7ed;
  padding: 8px 16px;
  border-radius: 12px 12px 0 0;
  display: flex;
  align-items: center;
}

.heart-icon {
  width: 20px;
  height: 20px;
  color: #52c41a;
  margin-right: 8px;
}

.title-text {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.monitor-subtitle {
  font-size: 14px;
  color: #666;
  margin-bottom: 20px;
  padding: 0 4px;
}

.heart-rate-data {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.rate-display {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.rate-value {
  font-size: 56px;
  font-weight: bold;
  color: #333;
  line-height: 1;
  transition: color 0.5s ease;
}

.rate-unit {
  font-size: 24px;
  color: #666;
  vertical-align: super;
}

.status-indicator {
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: bold;
  transition: color 0.5s ease;
}

.status-normal {
  background-color: #e6f7ed;
}

.status-slow {
  background-color: #f6ffed;
}

.status-fast {
  background-color: #fff1f0;
}

.abnormal-text {
  background-color: transparent !important;
  color: inherit !important;
}

.heart-rate-scale {
  position: relative;
  height: 60px;
}

.scale-container {
  height: 8px;
  background-color: #f0f0f0;
  border-radius: 4px;
  position: absolute;
  top: 26px;
  left: 12px;
  right: 12px;
  overflow: hidden;
}

.scale-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease, background-color 0.5s ease;
}

.scale-marks {
  display: flex;
  justify-content: space-between;
  position: absolute;
  top: 52px;
  left: 0;
  right: 0;
}

.scale-mark {
  font-size: 12px;
  color: #999;
  transform: translateX(-50%);
}
</style>