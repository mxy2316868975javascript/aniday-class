<template>
  <div class="login-container" :style="backgroundStyle">
    <div class="login-overlay"></div>

    <section class="login-hero">
      <p class="hero-kicker">Academic Console</p>
      <h1>{{ settings.system_name }}</h1>
      <p class="hero-summary">{{ settings.system_intro }}</p>

      <div class="hero-points">
        <div class="hero-point">
          <span class="hero-point-label">管理端语气</span>
          <strong>可信、秩序、效率</strong>
        </div>
        <div class="hero-point">
          <span class="hero-point-label">界面原则</span>
          <strong>学院精致感 + 高可读数据结构</strong>
        </div>
        <div class="hero-point">
          <span class="hero-point-label">默认账号</span>
          <strong>admin / admin123</strong>
        </div>
      </div>
    </section>

    <div class="login-card">
      <div class="login-card-header">
        <div class="brand-lockup">
          <div class="brand-seal">
            <img v-if="settings.system_logo" :src="settings.system_logo" alt="Logo" class="system-logo" />
            <span v-else>学</span>
          </div>
          <div>
            <p class="brand-kicker">Campus Sign In</p>
            <h2>进入教学运营中枢</h2>
          </div>
        </div>
        <el-tag effect="light" type="warning">Light / Dark Ready</el-tag>
      </div>

      <el-form :model="form" :rules="rules" ref="formRef" class="login-form">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名 / Username" :prefix-icon="User" size="large" clearable />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码 / Password"
            :prefix-icon="Lock"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <div class="login-form-actions">
          <el-button type="primary" size="large" :loading="loading" @click="handleLogin" class="login-btn">
            {{ loading ? '登录中...' : '登 录' }}
          </el-button>
          <el-button plain size="large" class="theme-btn" @click="handleThemeToggle">
            <el-icon><Moon v-if="theme === 'light'" /><Sunny v-else /></el-icon>
            {{ theme === 'light' ? '深色主题' : '浅色主题' }}
          </el-button>
        </div>
      </el-form>

      <div class="login-footnotes">
        <div class="login-tip">
          <el-icon><InfoFilled /></el-icon>
          <span>推荐使用班主任、管理员或任课教师账号进入系统</span>
        </div>
        <div class="login-tip">
          <el-icon><Document /></el-icon>
          <span>{{ settings.copyright }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Document, InfoFilled, Lock, Moon, Sunny, User } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { resolveTheme, toggleTheme } from '@/utils/theme'
import axios from 'axios'

const api = axios.create({ baseURL: '/api' })
const router = useRouter()
const userStore = useUserStore()

const formRef = ref(null)
const loading = ref(false)
const theme = ref(resolveTheme())

const settings = ref({
  system_name: 'Aniday Class 班级管理系统',
  system_logo: '',
  system_intro: '一个现代化的班级管理系统',
  login_background: '',
  copyright: '© 2024 Aniday Class',
  use_bing_background: true
})

const bingBackground = ref('')

const backgroundStyle = computed(() => {
  const image = settings.value.use_bing_background ? bingBackground.value : settings.value.login_background

  if (image) {
    return {
      backgroundImage:
        `linear-gradient(130deg, rgba(18, 28, 43, 0.78), rgba(31, 58, 95, 0.72)), url(${image})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center'
    }
  }

  return {}
})

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const fetchBingBackground = async () => {
  try {
    const res = await api.get('/bing-background')
    if (res.data.url) {
      bingBackground.value = res.data.url
    }
  } catch (error) {
    console.error('获取 Bing 背景失败', error)
  }
}

const fetchSettings = async () => {
  try {
    const res = await api.get('/settings/public')
    settings.value = {
      ...settings.value,
      ...res.data
    }
    document.title = res.data.system_name
  } catch (error) {
    console.error('获取系统设置失败', error)
  }
}

const handleLogin = async () => {
  await formRef.value.validate(async valid => {
    if (!valid) return

    loading.value = true
    try {
      await userStore.login(form.username, form.password)
      ElMessage.success('登录成功')
      router.push('/')
    } catch (error) {
      console.error(error)
      ElMessage.error('登录失败，请检查用户名和密码')
    } finally {
      loading.value = false
    }
  })
}

const handleThemeToggle = () => {
  theme.value = toggleTheme()
}

onMounted(async () => {
  theme.value = resolveTheme()
  await Promise.all([fetchSettings(), fetchBingBackground()])
})
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  padding: clamp(1.25rem, 2vw, 2rem);
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(360px, 460px);
  align-items: center;
  gap: clamp(1.5rem, 3vw, 4rem);
  background:
    radial-gradient(circle at top left, rgba(185, 138, 66, 0.18), transparent 30%),
    radial-gradient(circle at bottom left, rgba(124, 153, 140, 0.14), transparent 26%),
    linear-gradient(160deg, #132133 0%, #1f3550 45%, #243b54 100%);
  position: relative;
  overflow: hidden;
}

.login-overlay {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(120deg, transparent 0%, rgba(255, 255, 255, 0.06) 48%, transparent 100%);
  pointer-events: none;
}

.login-hero,
.login-card {
  position: relative;
  z-index: 1;
}

.login-hero {
  color: rgba(248, 244, 236, 0.94);
  padding-inline: clamp(0rem, 2vw, 2rem);
}

.login-hero h1 {
  margin: 0.75rem 0 1rem;
  font-family: var(--font-display);
  font-size: clamp(2.8rem, 4vw, 4.5rem);
  line-height: 1.04;
  max-width: 12ch;
}

.hero-summary {
  max-width: 40rem;
  color: rgba(248, 244, 236, 0.78);
  font-size: 1.02rem;
  line-height: 1.75;
}

.hero-points {
  margin-top: 2rem;
  display: grid;
  gap: 0.9rem;
  max-width: 32rem;
}

.hero-point {
  display: grid;
  gap: 0.2rem;
  padding: 1rem 1.15rem;
  border-radius: 1.25rem;
  background: rgba(248, 244, 236, 0.08);
  border: 1px solid rgba(248, 244, 236, 0.14);
  backdrop-filter: blur(12px);
}

.hero-point-label,
.brand-kicker {
  font-size: 0.78rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: rgba(248, 244, 236, 0.7);
}

.login-card {
  padding: clamp(1.35rem, 1rem + 1vw, 2rem);
  border-radius: 2rem;
  background: color-mix(in srgb, var(--surface-panel) 82%, rgba(255, 255, 255, 0.1) 18%);
  border: 1px solid rgba(255, 255, 255, 0.16);
  box-shadow: 0 28px 70px rgba(10, 17, 28, 0.34);
  backdrop-filter: blur(16px);
}

.login-card-header {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.brand-lockup {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.brand-seal {
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 1.2rem;
  display: grid;
  place-items: center;
  background: linear-gradient(145deg, color-mix(in srgb, var(--color-accent) 62%, white 38%) 0%, color-mix(in srgb, var(--color-primary) 76%, black 24%) 100%);
  color: var(--text-inverse);
  font-family: var(--font-display);
  font-size: 1.4rem;
}

.system-logo {
  max-width: 2rem;
  max-height: 2rem;
  object-fit: contain;
}

.brand-lockup h2 {
  margin: 0.25rem 0 0;
  font-family: var(--font-display);
  color: var(--text-primary);
}

.login-form {
  display: grid;
  gap: 0.4rem;
}

.login-form-actions {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.8rem;
}

.login-btn {
  min-height: 3.25rem;
}

.theme-btn {
  min-height: 3.25rem;
}

.login-footnotes {
  margin-top: 1.2rem;
  display: grid;
  gap: 0.65rem;
}

.login-tip {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  color: var(--text-secondary);
  font-size: 0.92rem;
}

@media (max-width: 1080px) {
  .login-container {
    grid-template-columns: 1fr;
    align-items: stretch;
  }

  .login-hero {
    padding-top: 3rem;
  }
}

@media (max-width: 720px) {
  .login-container {
    padding: 1rem;
  }

  .login-card-header,
  .login-form-actions {
    grid-template-columns: 1fr;
    display: grid;
  }

  .login-card {
    border-radius: 1.5rem;
  }

  .login-hero h1 {
    font-size: 2.4rem;
  }
}
</style>
