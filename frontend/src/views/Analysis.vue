<template>
  <div class="analysis page-grid">
    <PageHeader eyebrow="Insight Studio" title="数据分析" subtitle="围绕学期维度观察科目差异、分布区间和考试类型趋势。">
      <template #actions>
        <el-select v-model="semester" placeholder="选择学期" @change="loadData" style="width: 150px;">
          <el-option label="全部" value="" />
          <el-option label="2024-1" value="2024-1" />
          <el-option label="2024-2" value="2024-2" />
        </el-select>
      </template>
    </PageHeader>

    <el-row :gutter="20">
      <el-col :span="12">
        <SectionCard title="各科目平均成绩" description="用环形图对比学科整体表现。">
          <h3>各科目平均成绩</h3>
          <div ref="subjectChartRef" style="height: 350px;"></div>
        </SectionCard>
      </el-col>
      <el-col :span="12">
        <SectionCard title="成绩分布" description="比较科目最高分、平均分与最低分。">
          <h3>成绩分布</h3>
          <div ref="distributionChartRef" style="height: 350px;"></div>
        </SectionCard>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <SectionCard title="科目成绩详情" description="查看各科目人数与分值区间。">
          <h3>科目成绩详情</h3>
          <el-table :data="subjectAnalysis" style="width: 100%">
            <el-table-column prop="subject_name" label="科目" />
            <el-table-column prop="avg_score" label="平均分" />
            <el-table-column prop="max_score" label="最高分" />
            <el-table-column prop="min_score" label="最低分" />
            <el-table-column prop="count" label="考试人数" />
          </el-table>
        </SectionCard>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <SectionCard title="考试类型趋势" description="用趋势图观察不同考试类型的平均成绩变化。">
          <h3>考试类型趋势</h3>
          <div ref="trendChartRef" style="height: 350px;"></div>
        </SectionCard>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import api from '@/api'
import PageHeader from '@/components/ui/PageHeader.vue'
import SectionCard from '@/components/ui/SectionCard.vue'

const semester = ref('')
const subjectAnalysis = ref([])
const trends = ref({})

const subjectChartRef = ref(null)
const distributionChartRef = ref(null)
const trendChartRef = ref(null)
let subjectChart = null
let distributionChart = null
let trendChart = null

const loadData = async () => {
  const analysisData = await api.dashboard.getSubjectAnalysis({ semester: semester.value })
  subjectAnalysis.value = analysisData || []
  updateSubjectChart()
  updateDistributionChart()
  
  const trendData = await api.dashboard.getTrends({ semester: semester.value })
  trends.value = trendData || {}
  updateTrendChart()
}

const updateSubjectChart = () => {
  if (!subjectChart || subjectAnalysis.value.length === 0) return
  
  const data = subjectAnalysis.value.map(s => ({
    name: s.subject_name,
    value: s.avg_score
  }))
  
  subjectChart.setOption({
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      data: data,
      label: {
        formatter: '{b}: {c}分'
      }
    }]
  })
}

const updateDistributionChart = () => {
  if (!distributionChart || subjectAnalysis.value.length === 0) return
  
  const subjects = subjectAnalysis.value.map(s => s.subject_name)
  const maxScores = subjectAnalysis.value.map(s => s.max_score)
  const minScores = subjectAnalysis.value.map(s => s.min_score)
  const avgScores = subjectAnalysis.value.map(s => s.avg_score)
  
  distributionChart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: ['最高分', '平均分', '最低分'] },
    xAxis: { type: 'category', data: subjects },
    yAxis: { type: 'value', min: 0, max: 100 },
    series: [
      { name: '最高分', type: 'bar', data: maxScores, itemStyle: { color: '#67c23a' } },
      { name: '平均分', type: 'bar', data: avgScores, itemStyle: { color: '#409eff' } },
      { name: '最低分', type: 'bar', data: minScores, itemStyle: { color: '#f56c6c' } }
    ]
  })
}

const updateTrendChart = () => {
  if (!trendChart || Object.keys(trends.value).length === 0) return
  
  const examTypes = Object.keys(trends.value)
  const avgs = examTypes.map(t => trends.value[t].avg)
  
  trendChart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { 
      type: 'category', 
      data: examTypes.map(t => {
        const map = { midterm: '期中', final: '期末', monthly: '月考', quiz: '测验' }
        return map[t] || t
      }) 
    },
    yAxis: { type: 'value', min: 0, max: 100 },
    series: [{
      type: 'line',
      data: avgs,
      smooth: true,
      itemStyle: { color: '#409eff' },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(64, 158, 255, 0.5)' },
            { offset: 1, color: 'rgba(64, 158, 255, 0.1)' }
          ]
        }
      }
    }]
  })
}

watch(semester, () => loadData())

onMounted(async () => {
  await loadData()
  
  subjectChart = echarts.init(subjectChartRef.value)
  distributionChart = echarts.init(distributionChartRef.value)
  trendChart = echarts.init(trendChartRef.value)
  
  updateSubjectChart()
  updateDistributionChart()
  updateTrendChart()
  
  window.addEventListener('resize', () => {
    subjectChart?.resize()
    distributionChart?.resize()
    trendChart?.resize()
  })
})
</script>

<style scoped>
.analysis :deep(.section-card h3) {
  margin-bottom: 15px;
}
</style>
