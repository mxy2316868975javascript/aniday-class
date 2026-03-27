<template>
  <div class="portal-page">
    <section class="portal-hero">
      <div class="hero-header">
        <div>
          <p class="portal-kicker">Student Snapshot</p>
          <h1>{{ studentName }}</h1>
          <p class="hero-subtitle">{{ className }}</p>
        </div>
        <el-button circle plain class="hero-action" @click="handleLogout">
          <el-icon><SwitchButton /></el-icon>
        </el-button>
      </div>
    </section>

    <main class="home-main portal-grid">
      <section class="portal-actions-grid">
        <div class="portal-stat" @click="router.push('/scores')">
          <span class="portal-kicker portal-muted">平均成绩</span>
          <strong>{{ stats.average_score || '-' }}</strong>
          <p>查看最近考试记录与学期变化</p>
        </div>
        <div class="portal-stat" @click="router.push('/home')">
          <span class="portal-kicker portal-muted">出勤率</span>
          <strong>{{ stats.attendance_rate || '-' }}%</strong>
          <p>关注日常出勤与异常状态</p>
        </div>
        <div class="portal-stat" @click="router.push('/notifications')">
          <span class="portal-kicker portal-muted">通知入口</span>
          <strong>班级通知</strong>
          <p>第一时间接收学校与班级消息</p>
        </div>
      </section>

      <section class="portal-actions-grid">
        <div class="portal-card menu-card" @click="router.push('/scores')">
          <el-icon size="28" color="var(--color-primary)"><TrendCharts /></el-icon>
          <span>成绩查询</span>
        </div>
        <div class="portal-card menu-card" @click="router.push('/notifications')">
          <el-icon size="28" color="var(--color-sage)"><Bell /></el-icon>
          <span>班级通知</span>
        </div>
        <div class="portal-card menu-card" @click="router.push('/homework')">
          <el-icon size="28" color="var(--color-accent)"><Document /></el-icon>
          <span>班级作业</span>
        </div>
      </section>

      <section class="portal-panel">
        <div class="section-header">
          <div>
            <p class="portal-kicker portal-muted">Latest Scores</p>
            <h3 class="portal-section-title">最近成绩</h3>
          </div>
          <el-button text @click="router.push('/scores')">
            查看全部
            <el-icon><ArrowRight /></el-icon>
          </el-button>
        </div>

        <div class="portal-list" v-if="recentScores.length > 0">
          <article class="portal-list-card score-item" v-for="item in recentScores" :key="item.id">
            <div class="score-copy">
              <strong>{{ item.subject_name }}</strong>
              <span class="portal-muted">{{ getExamTypeText(item.exam_type) }}</span>
            </div>
            <span class="portal-score-chip">{{ item.score }}</span>
          </article>
        </div>

        <el-empty v-else description="暂无成绩记录" :image-size="80" />
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Bell, Document, TrendCharts, SwitchButton, ArrowRight } from '@element-plus/icons-vue'
import api from '@/api'

const router = useRouter()
const parentCode = localStorage.getItem('parent_code')
const studentName = localStorage.getItem('student_name')
const className = localStorage.getItem('class_name')
const stats = ref({})
const recentScores = ref([])

const fetchStats = async () => {
  try {
    const data = await api.getStats(parentCode)
    stats.value = data
  } catch (error) {
    console.error('获取统计失败', error)
  }
}

const fetchRecentScores = async () => {
  try {
    const data = await api.getScores(parentCode, { page: 1, page_size: 5 })
    recentScores.value = data.scores
  } catch (error) {
    console.error('获取成绩失败', error)
  }
}

const handleLogout = () => {
  localStorage.clear()
  router.push('/login')
}

const getExamTypeText = type => {
  const map = { midterm: '期中', final: '期末', quiz: '测验', exam: '考试' }
  return map[type] || type
}

onMounted(() => {
  fetchStats()
  fetchRecentScores()
})
</script>

<style scoped>
.hero-header {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: flex-start;
}

.hero-subtitle {
  margin-top: 0.4rem;
  color: rgba(248, 244, 236, 0.82);
}

.hero-action {
  color: var(--text-inverse);
  border-color: rgba(248, 244, 236, 0.2);
  background: rgba(248, 244, 236, 0.08);
}

.home-main {
  padding: 1rem;
  margin-top: -1.5rem;
}

.portal-stat {
  padding: 1rem;
  border-radius: 1.35rem;
  background: color-mix(in srgb, var(--surface-card) 96%, transparent);
  border: 1px solid var(--border-soft);
  box-shadow: var(--shadow-card);
}

.portal-stat strong {
  display: block;
  margin: 0.35rem 0 0.4rem;
  font-size: 1.45rem;
  color: var(--text-primary);
}

.portal-stat p {
  margin: 0;
  color: var(--text-secondary);
  line-height: 1.65;
  font-size: 0.9rem;
}

.menu-card {
  text-align: center;
  display: grid;
  gap: 0.6rem;
  place-items: center;
  min-height: 6rem;
}

.menu-card span {
  color: var(--text-primary);
  font-weight: 600;
}

.section-header {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: center;
  margin-bottom: 0.9rem;
}

.section-header h3 {
  margin: 0.15rem 0 0;
}

.score-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.score-copy {
  display: grid;
  gap: 0.25rem;
}

.score-copy strong {
  color: var(--text-primary);
}
</style>
