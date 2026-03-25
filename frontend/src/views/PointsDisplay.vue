<template>
  <div class="display-container" :class="{ 'fullscreen-mode': isFullscreen }">
    <div class="header">
      <h1>🏆 积分龙虎榜 🏆</h1>
      <p class="subtitle">{{ currentDateTime }}</p>
    </div>

    <div class="content">
      <div class="top3-section">
        <div class="podium">
          <div class="second-place" v-if="ranking[1]">
            <div class="avatar">🥈</div>
            <div class="rank-badge">2</div>
            <div class="name">{{ ranking[1].student_name }}</div>
            <div class="class">{{ ranking[1].class_name }}</div>
            <div class="points">{{ ranking[1].total_points }}</div>
          </div>
          <div class="first-place" v-if="ranking[0]">
            <div class="crown">👑</div>
            <div class="avatar">🥇</div>
            <div class="rank-badge">1</div>
            <div class="name">{{ ranking[0].student_name }}</div>
            <div class="class">{{ ranking[0].class_name }}</div>
            <div class="points">{{ ranking[0].total_points }}</div>
          </div>
          <div class="third-place" v-if="ranking[2]">
            <div class="avatar">🥉</div>
            <div class="rank-badge">3</div>
            <div class="name">{{ ranking[2].student_name }}</div>
            <div class="class">{{ ranking[2].class_name }}</div>
            <div class="points">{{ ranking[2].total_points }}</div>
          </div>
        </div>
      </div>

      <div class="stats-section">
        <div class="stat-card">
          <div class="stat-icon">👥</div>
          <div class="stat-value">{{ stats.total_students }}</div>
          <div class="stat-label">参与学生</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">⭐</div>
          <div class="stat-value">{{ stats.total_points_distributed }}</div>
          <div class="stat-label">积分发放</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🎁</div>
          <div class="stat-value">{{ stats.total_points_exchanged }}</div>
          <div class="stat-label">积分兑换</div>
        </div>
      </div>

      <div class="list-section">
        <div class="list-header">
          <span>排名</span>
          <span>姓名</span>
          <span>班级</span>
          <span>积分</span>
        </div>
        <div class="list-content">
          <div v-for="(item, index) in ranking.slice(3)" :key="index" class="list-item">
            <div class="item-rank">{{ index + 4 }}</div>
            <div class="item-name">{{ item.student_name }}</div>
            <div class="item-class">{{ item.class_name }}</div>
            <div class="item-points">{{ item.total_points }}</div>
          </div>
        </div>
      </div>
    </div>

    <div class="footer">
      <button @click="toggleFullscreen" class="fullscreen-btn">
        {{ isFullscreen ? '退出全屏' : '全屏展示' }}
      </button>
      <button @click="refresh" class="refresh-btn">刷新数据</button>
    </div>

    <div class="celebration" v-if="showCelebration">
      <div class="confetti"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

const api = axios.create({ baseURL: '/api' })
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

const ranking = ref([])
const stats = ref({ total_students: 0, active_students: 0, total_points_distributed: 0, total_points_exchanged: 0 })
const currentDateTime = ref('')
const isFullscreen = ref(false)
const showCelebration = ref(false)
let timer = null

const updateDateTime = () => {
  const now = new Date()
  currentDateTime.value = now.toLocaleString('zh-CN', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const fetchData = async () => {
  try {
    const [statsRes, rankingRes] = await Promise.all([
      api.get('/points/stats'),
      api.get('/points/ranking?limit=20')
    ])
    stats.value = statsRes.data
    ranking.value = rankingRes.data
  } catch (e) {
    console.error('获取数据失败', e)
  }
}

const toggleFullscreen = async () => {
  if (!document.fullscreenElement) {
    await document.documentElement.requestFullscreen()
    isFullscreen.value = true
  } else {
    await document.exitFullscreen()
    isFullscreen.value = false
  }
}

const refresh = () => {
  fetchData()
  showCelebration.value = true
  setTimeout(() => {
    showCelebration.value = false
  }, 3000)
}

onMounted(() => {
  updateDateTime()
  fetchData()
  timer = setInterval(() => {
    updateDateTime()
    fetchData()
  }, 30000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
.display-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  box-sizing: border-box;
}

.display-container.fullscreen-mode {
  padding: 40px;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 48px;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.subtitle {
  font-size: 20px;
  opacity: 0.9;
  margin-top: 10px;
}

.content {
  max-width: 1200px;
  margin: 0 auto;
}

.podium {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  gap: 20px;
  margin-bottom: 40px;
}

.first-place {
  order: 2;
  text-align: center;
}

.first-place .avatar {
  font-size: 80px;
  line-height: 80px;
}

.first-place .rank-badge {
  background: linear-gradient(135deg, #ffd700, #ffb347);
  color: #333;
  font-size: 24px;
  font-weight: bold;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 10px auto;
}

.first-place .name {
  font-size: 28px;
  font-weight: bold;
}

.first-place .points {
  font-size: 48px;
  color: #ffd700;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.second-place, .third-place {
  text-align: center;
}

.second-place .avatar, .third-place .avatar {
  font-size: 60px;
}

.second-place .rank-badge, .third-place .rank-badge {
  background: #fff;
  color: #333;
  font-size: 20px;
  font-weight: bold;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 8px auto;
}

.second-place .name, .third-place .name {
  font-size: 22px;
  font-weight: bold;
}

.second-place .points, .third-place .points {
  font-size: 36px;
  color: #ffd700;
}

.class {
  font-size: 14px;
  opacity: 0.8;
  margin-top: 5px;
}

.stats-section {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-bottom: 40px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 30px 50px;
  text-align: center;
  backdrop-filter: blur(10px);
}

.stat-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 36px;
  font-weight: bold;
}

.stat-label {
  font-size: 16px;
  opacity: 0.9;
  margin-top: 5px;
}

.list-section {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

.list-header {
  display: grid;
  grid-template-columns: 80px 1fr 1fr 100px;
  background: rgba(255, 255, 255, 0.3);
  padding: 15px 30px;
  font-weight: bold;
  font-size: 18px;
}

.list-content {
  max-height: 300px;
  overflow-y: auto;
}

.list-item {
  display: grid;
  grid-template-columns: 80px 1fr 1fr 100px;
  padding: 12px 30px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transition: background 0.3s;
}

.list-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.list-item:nth-child(odd) {
  background: rgba(255, 255, 255, 0.05);
}

.item-rank {
  font-weight: bold;
  color: #ffd700;
}

.item-name {
  font-weight: bold;
}

.item-points {
  color: #ffd700;
  font-weight: bold;
}

.footer {
  text-align: center;
  margin-top: 30px;
}

.fullscreen-btn, .refresh-btn {
  background: white;
  color: #667eea;
  border: none;
  padding: 12px 30px;
  font-size: 16px;
  border-radius: 25px;
  cursor: pointer;
  margin: 0 10px;
  transition: transform 0.2s;
}

.fullscreen-btn:hover, .refresh-btn:hover {
  transform: scale(1.05);
}

.celebration {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1000;
}

.confetti {
  width: 100%;
  height: 100%;
  background: url('data:image/svg+xml,...');
  animation: confetti 3s ease-out;
}

@keyframes confetti {
  0% { opacity: 1; }
  100% { opacity: 0; }
}
</style>
