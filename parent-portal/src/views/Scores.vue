<template>
  <div class="portal-page">
    <div class="portal-topbar">
      <el-button text @click="router.push('/home')">
        <el-icon><ArrowLeft /></el-icon>
      </el-button>
      <h2>成绩查询</h2>
    </div>
    <div class="portal-card filter-row">
      <el-select v-model="semester" placeholder="选择学期" @change="fetchScores" size="default" style="width: 100%;">
        <el-option label="全部学期" value="" />
        <el-option label="2025-2" value="2025-2" />
        <el-option label="2025-1" value="2025-1" />
        <el-option label="2024-2" value="2024-2" />
        <el-option label="2024-1" value="2024-1" />
      </el-select>
    </div>

    <div class="stats-row portal-actions-grid">
      <div class="portal-stat stat-item">
        <span class="value">{{ totalExams }}</span>
        <span class="label">考试次数</span>
      </div>
      <div class="portal-stat stat-item">
        <span class="value">{{ averageScore }}</span>
        <span class="label">平均成绩</span>
      </div>
    </div>

    <div class="score-list portal-list" v-loading="loading">
      <div class="score-card portal-list-card" v-for="item in scores" :key="item.id">
        <div class="score-header">
          <span class="subject">{{ item.subject_name }}</span>
          <span class="portal-score-chip">{{ item.score }}</span>
        </div>
        <div class="score-info">
          <span>{{ getExamTypeText(item.exam_type) }}</span>
          <span>{{ formatDate(item.exam_date) }}</span>
          <span>{{ item.semester }}</span>
        </div>
      </div>

      <el-empty v-if="scores.length === 0 && !loading" description="暂无成绩记录" />

      <el-pagination
        v-if="total > 0"
        v-model:current-page="page"
        :total="total"
        :page-size="pageSize"
        layout="prev, pager, next"
        @current-change="fetchScores"
        style="margin-top: 20px; justify-content: center"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import api from '@/api'

const router = useRouter()
const loading = ref(false)
const parentCode = localStorage.getItem('parent_code')

const scores = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const semester = ref('')

const totalExams = computed(() => total.value)
const averageScore = computed(() => {
  if (scores.value.length === 0) return '-'
  const validScores = scores.value.filter(s => s.score)
  if (validScores.length === 0) return '-'
  const avg = validScores.reduce((sum, s) => sum + s.score, 0) / validScores.length
  return avg.toFixed(1)
})

const fetchScores = async () => {
  loading.value = true
  try {
    const data = await api.getScores(parentCode, {
      semester: semester.value,
      page: page.value,
      page_size: pageSize.value
    })
    scores.value = data.scores
    total.value = data.total
  } catch (e) {
    console.error('获取成绩失败', e)
  } finally {
    loading.value = false
  }
}

const getScoreType = (score) => {
  if (score >= 90) return 'success'
  if (score >= 80) return ''
  if (score >= 60) return 'warning'
  return 'danger'
}

const getExamTypeText = (type) => {
  const map = { midterm: '期中', final: '期末', quiz: '测验', exam: '考试' }
  return map[type] || type
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN')
}

onMounted(() => {
  fetchScores()
})
</script>

<style scoped>
.filter-row {
  margin: 1rem;
}

.stats-row {
  margin: 0 1rem 1rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 6.8rem;
}

.stat-item .value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-item .label {
  font-size: 0.92rem;
  color: var(--text-secondary);
  margin-top: 6px;
}

.score-list {
  padding: 0 1rem 1rem;
}

.score-card {
  margin-bottom: 0;
}

.score-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.score-header .subject {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.score-info {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: var(--text-secondary);
}
</style>
