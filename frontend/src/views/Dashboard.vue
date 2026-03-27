<template>
  <div class="page-grid">
    <PageHeader
      eyebrow="Operations Overview"
      title="数据仪表盘"
      subtitle="从学生、班级、成绩与考勤四个维度快速判断当前教学运营状态。"
    >
      <template #actions>
        <div class="table-toolbar">
          <div class="metric-badge">
            <el-icon><Collection /></el-icon>
            <span>当前学期：{{ semester || '全部' }}</span>
          </div>
          <el-select v-model="semester" placeholder="选择学期" @change="handleSemesterChange" style="width: 200px">
            <el-option label="全部学期" value="" />
            <el-option v-for="s in semesters" :key="s.value" :label="s.label" :value="s.value" />
          </el-select>
        </div>
      </template>
    </PageHeader>

    <section class="stats-grid">
      <StatCard label="学生总数" :value="stats.total_students" meta="覆盖当前可见班级学生档案" tone="primary">
        <template #icon><el-icon><User /></el-icon></template>
      </StatCard>
      <StatCard label="班级数量" :value="stats.total_classes" meta="含系统可访问的全部班级" tone="success">
        <template #icon><el-icon><School /></el-icon></template>
      </StatCard>
      <StatCard label="成绩记录" :value="stats.total_scores" meta="已录入成绩总条数" tone="warning">
        <template #icon><el-icon><Document /></el-icon></template>
      </StatCard>
      <StatCard label="考勤率" :value="`${stats.attendance_rate}%`" meta="最近统计周期整体表现" tone="danger">
        <template #icon><el-icon><Calendar /></el-icon></template>
      </StatCard>
    </section>

    <section class="section-row">
      <SectionCard class="section-span-7" title="平均分观察" description="用仪表盘快速观察当前学期的整体学业水位。">
        <div ref="scoreChartRef" class="chart-shell"></div>
      </SectionCard>

      <SectionCard class="section-span-5" title="最近成绩记录" description="帮助老师快速确认近期录入数据是否正常。">
        <el-table :data="stats.recent_scores" height="320" empty-text="暂无成绩记录">
          <el-table-column prop="student_name" label="学生" min-width="120" />
          <el-table-column prop="subject_name" label="科目" min-width="90" />
          <el-table-column prop="score" label="成绩" width="88">
            <template #default="{ row }">
              <StatusBadge :type="getScoreTone(row.score)" :label="row.score" />
            </template>
          </el-table-column>
          <el-table-column prop="exam_type" label="考试类型" min-width="110" />
        </el-table>
      </SectionCard>
    </section>

    <section class="section-row">
      <SectionCard class="section-span-8" title="班级平均成绩排名" description="用于识别高表现班级与需要支持的班级。">
        <div ref="rankingChartRef" class="chart-shell"></div>
      </SectionCard>

      <SectionCard class="section-span-4" title="教务提示" description="把关键指标翻译成可快速理解的运营语句。">
        <div class="dashboard-notes">
          <div class="dashboard-note">
            <span class="note-label">平均分</span>
            <strong>{{ stats.avg_score }} 分</strong>
            <p>如果平均分波动明显，优先查看近期考试类型和班级差异。</p>
          </div>
          <div class="dashboard-note">
            <span class="note-label">考勤</span>
            <strong>{{ stats.attendance_rate }}%</strong>
            <p>考勤率异常时建议联动班级排名与学生名单排查问题来源。</p>
          </div>
        </div>
      </SectionCard>
    </section>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import * as echarts from 'echarts'
import api from '@/api'
import PageHeader from '@/components/ui/PageHeader.vue'
import SectionCard from '@/components/ui/SectionCard.vue'
import StatCard from '@/components/ui/StatCard.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import { Calendar, Collection, Document, School, User } from '@element-plus/icons-vue'

const semester = ref('')
const semesters = ref([])
const stats = reactive({
  total_students: 0,
  total_classes: 0,
  total_scores: 0,
  avg_score: 0,
  attendance_rate: 0,
  recent_scores: [],
  class_rankings: []
})

const scoreChartRef = ref(null)
const rankingChartRef = ref(null)
let scoreChart = null
let rankingChart = null

const loadSemesters = async () => {
  try {
    const data = await api.semesters.list()
    semesters.value = (data || []).map(item => ({
      label: item.name,
      value: item.name
    }))
  } catch (error) {
    console.error('加载学期失败', error)
    semesters.value = []
  }
}

const loadStats = async () => {
  try {
    const data = await api.dashboard.getStats({ semester: semester.value || undefined })
    if (data) {
      Object.assign(stats, data)
      updateScoreChart()
    }
  } catch (error) {
    console.error('加载统计数据失败', error)
  }
}

const loadRankings = async () => {
  try {
    const data = await api.dashboard.getClassRankings({ semester: semester.value || undefined })
    stats.class_rankings = (data || []).filter(item => item.class_id)
    updateRankingChart()
  } catch (error) {
    console.error('加载班级排名失败', error)
  }
}

const handleSemesterChange = async () => {
  await Promise.all([loadStats(), loadRankings()])
}

const getScoreTone = score => {
  if (score >= 90) return 'success'
  if (score >= 80) return 'warning'
  if (score >= 60) return 'info'
  return 'danger'
}

const updateScoreChart = () => {
  if (!scoreChart) return

  scoreChart.setOption({
    backgroundColor: 'transparent',
    series: [
      {
        type: 'gauge',
        startAngle: 210,
        endAngle: -30,
        min: 0,
        max: 100,
        progress: {
          show: true,
          width: 18,
          roundCap: true,
          itemStyle: {
            color: '#b98a42'
          }
        },
        axisLine: {
          lineStyle: {
            width: 18,
            color: [[1, 'rgba(120, 132, 146, 0.18)']]
          }
        },
        splitLine: {
          distance: -20,
          length: 12,
          lineStyle: {
            width: 2,
            color: 'rgba(86, 98, 112, 0.28)'
          }
        },
        axisTick: { show: false },
        axisLabel: {
          distance: 20,
          color: '#7d8897',
          fontSize: 12
        },
        pointer: {
          show: false
        },
        anchor: {
          show: false
        },
        detail: {
          valueAnimation: true,
          formatter: value => `${value} 分`,
          offsetCenter: [0, '14%'],
          color: '#243041',
          fontSize: 30,
          fontWeight: 700
        },
        title: {
          offsetCenter: [0, '-22%'],
          color: '#536073',
          fontSize: 14
        },
        data: [{ value: Number(stats.avg_score || 0), name: '平均成绩' }]
      }
    ]
  })
}

const updateRankingChart = () => {
  if (!rankingChart) return

  const xData = stats.class_rankings.map(item => item.class_name)
  const yData = stats.class_rankings.map(item => item.avg_score)

  rankingChart.setOption({
    backgroundColor: 'transparent',
    grid: {
      left: 40,
      right: 12,
      top: 20,
      bottom: 42
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(20, 28, 39, 0.9)',
      borderWidth: 0,
      textStyle: { color: '#f8f4ec' }
    },
    xAxis: {
      type: 'category',
      data: xData,
      axisLine: { lineStyle: { color: 'rgba(83, 96, 115, 0.24)' } },
      axisLabel: { color: '#536073' }
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 100,
      splitLine: { lineStyle: { color: 'rgba(83, 96, 115, 0.12)' } },
      axisLabel: { color: '#536073' }
    },
    series: [
      {
        type: 'bar',
        barWidth: 28,
        data: yData,
        itemStyle: {
          borderRadius: [14, 14, 6, 6],
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: '#b98a42' },
              { offset: 1, color: '#6a8577' }
            ]
          }
        }
      }
    ]
  })
}

onMounted(async () => {
  await Promise.all([loadSemesters(), loadStats(), loadRankings()])

  scoreChart = echarts.init(scoreChartRef.value)
  rankingChart = echarts.init(rankingChartRef.value)
  updateScoreChart()
  updateRankingChart()

  window.addEventListener('resize', () => {
    scoreChart?.resize()
    rankingChart?.resize()
  })
})
</script>

<style scoped>
.dashboard-notes {
  display: grid;
  gap: 1rem;
}

.dashboard-note {
  padding: 1.1rem;
  border-radius: var(--radius-md);
  background: color-mix(in srgb, var(--surface-subtle) 78%, transparent);
  border: 1px solid var(--border-soft);
}

.note-label {
  display: inline-block;
  margin-bottom: 0.4rem;
  color: var(--text-secondary);
  font-size: 0.82rem;
  letter-spacing: 0.08em;
}

.dashboard-note strong {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
  font-size: 1.45rem;
}

.dashboard-note p {
  margin: 0;
  color: var(--text-secondary);
  line-height: 1.7;
}
</style>
