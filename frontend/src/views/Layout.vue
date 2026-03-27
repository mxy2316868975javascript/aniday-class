<template>
  <el-container class="layout-container">
    <el-aside
      :width="isCollapsed ? '84px' : '278px'"
      class="sidebar"
      :class="{ 'sidebar-collapsed': isCollapsed, 'sidebar-transitioning': isTransitioning }"
    >
      <div class="sidebar-backdrop"></div>
      <div class="sidebar-inner">
        <div class="logo-card">
          <div class="logo-copy">
            <div class="logo-badge">
              <img v-if="userStore.systemSettings?.system_logo" :src="userStore.systemSettings.system_logo" alt="Logo" class="header-logo" />
              <el-icon v-else><School /></el-icon>
            </div>
            <transition name="fade-slide">
              <div v-if="!isCollapsed" class="logo-text-wrap">
                <h2 class="logo-text">{{ userStore.systemSettings?.system_name || '班级管理' }}</h2>
              </div>
            </transition>
          </div>

          <el-button class="collapse-btn" circle plain @click="toggleCollapse">
            <el-icon><Fold v-if="!isCollapsed" /><Expand v-else /></el-icon>
          </el-button>
        </div>

        <el-menu :default-active="activeMenu" :collapse="isCollapsed" router class="sidebar-menu">
          <el-tooltip
            v-for="item in menuItems"
            :key="item.index"
            :content="item.title"
            placement="right"
            :disabled="!isCollapsed"
            :show-after="120"
          >
            <el-menu-item :index="item.index">
              <el-icon><component :is="item.icon" /></el-icon>
              <template #title>
                <span class="menu-label">{{ item.title }}</span>
              </template>
            </el-menu-item>
          </el-tooltip>
        </el-menu>

        <div class="sidebar-footnote" v-if="!isCollapsed">
          <p>可信、克制、温暖</p>
        </div>
      </div>
    </el-aside>

    <el-container>
      <el-header class="header">
        <div class="header-left">
          <div class="eyebrow-title">
            <span class="hero-kicker">Campus Operations</span>
            <h3>{{ currentRouteName }}</h3>
          </div>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/dashboard' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentRouteName }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>

        <div class="header-right">
          <div class="header-toolbar">
            <el-tooltip :content="themeLabel" placement="bottom">
              <el-button circle plain class="theme-toggle" @click="handleThemeToggle">
                <el-icon><Moon v-if="theme === 'light'" /><Sunny v-else /></el-icon>
              </el-button>
            </el-tooltip>

            <el-dropdown @command="handleCommand">
              <div class="user-info">
                <el-avatar :size="38" class="user-avatar">
                  {{ userStore.userInfo?.real_name?.charAt(0) || 'U' }}
                </el-avatar>
                <div class="user-copy">
                  <span class="username">{{ userStore.userInfo?.real_name }}</span>
                  <span class="user-role">{{ getRoleText(userStore.userInfo?.role) }}</span>
                </div>
                <el-tag :type="getRoleTagType(userStore.userInfo?.role)" size="small">
                  {{ getRoleText(userStore.userInfo?.role) }}
                </el-tag>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="settings">
                    <el-icon><Setting /></el-icon>
                    系统设置
                  </el-dropdown-item>
                  <el-dropdown-item command="theme">
                    <el-icon><Moon /></el-icon>
                    切换主题
                  </el-dropdown-item>
                  <el-dropdown-item command="logout" divided>
                    <el-icon><SwitchButton /></el-icon>
                    退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>

      <el-main class="main-content">
        <div class="main-surface">
          <router-view />
        </div>
      </el-main>

      <el-footer class="footer">
        <div class="footer-content">
          <span>Aniday Class 校园运营中枢</span>
          <span>精致学院风 · {{ theme === 'light' ? 'Light' : 'Dark' }} Theme</span>
        </div>
      </el-footer>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Bell,
  Calendar,
  Clock,
  Coin,
  Collection,
  DataAnalysis,
  Document,
  Expand,
  Fold,
  Moon,
  PieChart,
  Reading,
  School,
  Setting,
  Sunny,
  SwitchButton,
  TrendCharts,
  User,
  UserFilled
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { resolveTheme, toggleTheme } from '@/utils/theme'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isCollapsed = ref(false)
const isTransitioning = ref(false)
const theme = ref(resolveTheme())
let collapseTimer = null

const activeMenu = computed(() => route.path)

const currentRouteName = computed(() => {
  const routeMap = {
    '/dashboard': '数据仪表盘',
    '/classes': '班级管理',
    '/students': '学生管理',
    '/scores': '成绩管理',
    '/attendance': '考勤管理',
    '/rankings': '班级排名',
    '/analysis': '数据分析',
    '/users': '用户管理',
    '/subjects': '科目管理',
    '/semesters': '学期管理',
    '/logs': '操作日志',
    '/points': '积分系统',
    '/points-display': '积分展示',
    '/settings': '系统设置',
    '/homework': '作业管理',
    '/notifications': '通知中心'
  }

  return routeMap[route.path] || '控制台'
})

const menuItems = computed(() => {
  const items = [
    { index: '/dashboard', title: '数据仪表盘', icon: DataAnalysis },
    { index: '/classes', title: '班级管理', icon: School, adminOnly: true },
    { index: '/students', title: '学生管理', icon: User },
    { index: '/scores', title: '成绩管理', icon: Document },
    { index: '/attendance', title: '考勤管理', icon: Calendar },
    { index: '/rankings', title: '班级排名', icon: TrendCharts },
    { index: '/analysis', title: '数据分析', icon: PieChart },
    { index: '/users', title: '用户管理', icon: UserFilled, adminOnly: true },
    { index: '/subjects', title: '科目管理', icon: Reading, adminOnly: true },
    { index: '/semesters', title: '学期管理', icon: Collection, adminOnly: true },
    { index: '/logs', title: '操作日志', icon: Clock, adminOnly: true },
    { index: '/points', title: '积分系统', icon: Coin },
    { index: '/homework', title: '作业管理', icon: Document },
    { index: '/notifications', title: '通知中心', icon: Bell },
    { index: '/settings', title: '系统设置', icon: Setting, adminOnly: true }
  ]

  return items.filter(item => !item.adminOnly || userStore.isAdmin)
})

const themeLabel = computed(() => theme.value === 'light' ? '切换到深色主题' : '切换到浅色主题')

const toggleCollapse = () => {
  isTransitioning.value = true
  isCollapsed.value = !isCollapsed.value

  if (collapseTimer) {
    clearTimeout(collapseTimer)
  }

  collapseTimer = window.setTimeout(() => {
    isTransitioning.value = false
  }, 380)
}

const getRoleText = (role) => {
  const roleMap = {
    admin: '管理员',
    class_teacher: '班主任',
    teacher: '任课教师'
  }
  return roleMap[role] || '未知角色'
}

const getRoleTagType = (role) => {
  const typeMap = {
    admin: 'danger',
    class_teacher: 'warning',
    teacher: 'success'
  }
  return typeMap[role] || 'info'
}

const handleThemeToggle = () => {
  theme.value = toggleTheme()
}

const handleCommand = (command) => {
  switch (command) {
    case 'settings':
      router.push('/settings')
      break
    case 'theme':
      handleThemeToggle()
      break
    case 'logout':
      userStore.logout()
      router.push('/login')
      break
    default:
      ElMessage.info('功能开发中...')
  }
}

onMounted(async () => {
  theme.value = resolveTheme()
  if (!userStore.systemSettings) {
    await userStore.fetchSystemSettings()
  }
})

onBeforeUnmount(() => {
  if (collapseTimer) {
    clearTimeout(collapseTimer)
  }
})
</script>

<style scoped>
.layout-container {
  min-height: 100vh;
}

.sidebar {
  position: relative;
  padding: 1rem;
  background:
    linear-gradient(180deg, color-mix(in srgb, var(--surface-inverse) 94%, black 6%) 0%, color-mix(in srgb, var(--surface-inverse) 82%, var(--color-primary) 18%) 100%);
  box-shadow: inset -18px 0 24px -24px rgba(248, 244, 236, 0.16);
  overflow: hidden;
  transition:
    width var(--motion-slow),
    padding var(--motion-base),
    box-shadow var(--motion-base);
  will-change: width;
}

.sidebar-transitioning {
  pointer-events: none;
}

.sidebar-backdrop {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at top, color-mix(in srgb, var(--color-accent) 18%, transparent) 0%, transparent 42%),
    radial-gradient(circle at bottom left, color-mix(in srgb, var(--color-sage) 18%, transparent) 0%, transparent 38%);
  opacity: 0.9;
  pointer-events: none;
}

.sidebar-inner {
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100%;
  gap: 1rem;
  min-height: 0;
  transition: gap var(--motion-base), transform var(--motion-base);
}

.logo-card {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  align-items: center;
  padding: 1rem;
  border-radius: var(--radius-lg);
  background: color-mix(in srgb, var(--surface-inverse) 82%, white 18%);
  border: 1px solid color-mix(in srgb, white 12%, transparent);
  box-shadow: 0 18px 36px rgba(0, 0, 0, 0.16);
  transition:
    padding var(--motion-base),
    border-radius var(--motion-base),
    gap var(--motion-base),
    transform var(--motion-base),
    box-shadow var(--motion-base);
}

.logo-copy {
  display: flex;
  align-items: center;
  gap: 0.9rem;
  min-width: 0;
  transition: gap var(--motion-base), justify-content var(--motion-base);
}

.logo-badge {
  width: 3rem;
  height: 3rem;
  border-radius: 1rem;
  display: grid;
  place-items: center;
  background: linear-gradient(145deg, color-mix(in srgb, var(--color-accent) 62%, white 38%) 0%, color-mix(in srgb, var(--color-primary) 74%, black 26%) 100%);
  color: var(--text-inverse);
  flex-shrink: 0;
  transition:
    width var(--motion-base),
    height var(--motion-base),
    border-radius var(--motion-base),
    transform var(--motion-base);
}

.header-logo {
  max-width: 1.8rem;
  max-height: 1.8rem;
  object-fit: contain;
}

.logo-kicker {
  margin: 0;
  color: color-mix(in srgb, var(--text-inverse) 76%, transparent);
  font-size: 0.72rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.logo-text {
  margin: 0.25rem 0 0;
  font-family: var(--font-display);
  font-size: 1.15rem;
  color: var(--text-inverse);
}

.logo-text-wrap {
  transition: opacity var(--motion-base), transform var(--motion-base), filter var(--motion-base);
}

.collapse-btn {
  border-color: color-mix(in srgb, white 14%, transparent);
  color: var(--text-inverse);
  background: color-mix(in srgb, white 10%, transparent);
  transition:
    transform var(--motion-fast),
    background-color var(--motion-fast),
    border-color var(--motion-fast),
    width var(--motion-base),
    height var(--motion-base);
}

.sidebar-menu {
  flex: 1;
  padding: 0.35rem;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: thin;
  scrollbar-color: transparent transparent;
  -ms-overflow-style: auto;
  transition: padding var(--motion-base);
}

.sidebar-menu::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}

.sidebar-menu::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-menu::-webkit-scrollbar-thumb {
  background: transparent;
  border-radius: 999px;
}

.sidebar-menu:hover {
  scrollbar-color: color-mix(in srgb, var(--text-inverse) 28%, transparent) transparent;
}

.sidebar-menu:hover::-webkit-scrollbar-thumb {
  background: color-mix(in srgb, var(--text-inverse) 28%, transparent);
}

.sidebar-menu:hover::-webkit-scrollbar-thumb:hover {
  background: color-mix(in srgb, var(--text-inverse) 42%, transparent);
}

.sidebar-menu :deep(.el-menu-item) {
  height: 3.25rem;
  margin: 0.25rem 0;
  border-radius: 1rem;
  color: color-mix(in srgb, var(--text-inverse) 78%, transparent) !important;
  font-weight: 500;
  transition:
    transform var(--motion-fast),
    background-color var(--motion-fast),
    color var(--motion-fast),
    width var(--motion-base),
    height var(--motion-base),
    margin var(--motion-base),
    border-radius var(--motion-base),
    padding var(--motion-base);
}

.sidebar-menu :deep(.el-menu-item:hover) {
  background: color-mix(in srgb, white 10%, transparent) !important;
  color: var(--text-inverse) !important;
  transform: translateX(4px);
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  background: linear-gradient(135deg, color-mix(in srgb, var(--color-accent) 54%, white 46%) 0%, color-mix(in srgb, var(--color-primary) 68%, black 32%) 100%) !important;
  color: var(--text-inverse) !important;
  box-shadow: 0 12px 26px rgba(0, 0, 0, 0.2);
}

.sidebar-menu :deep(.el-menu-item .el-icon) {
  color: inherit !important;
}

.sidebar-menu :deep(.menu-label) {
  display: inline-block;
  transition: opacity var(--motion-base), transform var(--motion-base), filter var(--motion-base);
  transform-origin: left center;
}

.sidebar-transitioning .logo-text-wrap,
.sidebar-transitioning .sidebar-menu :deep(.menu-label) {
  opacity: 0.22;
  filter: blur(1.5px);
}

.sidebar-collapsed {
  padding-inline: 0.75rem;
}

.sidebar-collapsed .sidebar-inner {
  align-items: center;
  gap: 0.85rem;
}

.sidebar-collapsed .logo-card {
  width: 100%;
  padding: 0.8rem 0.45rem;
  flex-direction: column;
  justify-content: center;
  gap: 0.75rem;
  border-radius: 1.9rem;
  transform: translateZ(0);
}

.sidebar-collapsed .logo-copy {
  width: 100%;
  justify-content: center;
}

.sidebar-collapsed .logo-badge {
  width: 3.4rem;
  height: 3.4rem;
  border-radius: 1.35rem;
  transform: scale(1.02);
}

.sidebar-collapsed .logo-text-wrap {
  opacity: 0;
  transform: translateX(-8px);
  filter: blur(2px);
}

.sidebar-collapsed .collapse-btn {
  width: 2.5rem;
  height: 2.5rem;
  margin: 0;
}

.sidebar-collapsed .sidebar-menu {
  width: 100%;
  padding: 0;
}

.sidebar-collapsed .sidebar-menu :deep(.el-menu) {
  width: 100%;
}

.sidebar-collapsed .sidebar-menu :deep(.el-menu-item) {
  width: 3.9rem;
  height: 3.9rem;
  margin: 0.35rem auto;
  padding: 0 !important;
  border-radius: 1.45rem;
  justify-content: center;
}

.sidebar-collapsed .sidebar-menu :deep(.el-menu-item:hover) {
  transform: none;
}

.sidebar-collapsed .sidebar-menu :deep(.el-menu-item.is-active) {
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.22);
}

.sidebar-collapsed .sidebar-menu :deep(.el-menu-item .el-icon) {
  margin-right: 0 !important;
  font-size: 1.3rem;
}

.sidebar-collapsed .sidebar-menu :deep(.menu-label) {
  opacity: 0;
  transform: translateX(-6px);
  filter: blur(2px);
}

.sidebar-footnote {
  padding: 1rem;
  border-radius: 1.35rem;
  background: color-mix(in srgb, white 8%, transparent);
  color: color-mix(in srgb, var(--text-inverse) 84%, transparent);
  border: 1px solid color-mix(in srgb, white 10%, transparent);
}

.sidebar-footnote p {
  margin: 0 0 0.25rem;
  font-family: var(--font-display);
}

.sidebar-footnote span {
  font-size: 0.82rem;
  color: color-mix(in srgb, var(--text-inverse) 66%, transparent);
}

.header {
  height: auto;
  padding: 1.2rem 1.5rem 0;
  background: transparent;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.header-left {
  display: grid;
  gap: 0.85rem;
}

.header-right {
  display: flex;
  justify-content: flex-end;
}

.header-toolbar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.7rem 0.85rem;
  background: color-mix(in srgb, var(--surface-card) 92%, transparent);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-pill);
  box-shadow: var(--shadow-card);
}

.social-links {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding-right: 0.35rem;
  margin-right: 0.35rem;
  border-right: 1px solid var(--border-soft);
}

.social-link,
.theme-toggle {
  width: 2.6rem;
  height: 2.6rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  color: var(--text-secondary);
}

.social-link:hover {
  color: var(--color-primary);
  background: color-mix(in srgb, var(--surface-subtle) 74%, transparent);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
}

.user-avatar {
  background: linear-gradient(135deg, var(--color-primary) 0%, color-mix(in srgb, var(--color-accent) 48%, var(--color-primary) 52%) 100%);
  color: var(--text-inverse);
}

.user-copy {
  display: grid;
}

.username {
  font-weight: 700;
  color: var(--text-primary);
}

.user-role {
  font-size: 0.82rem;
  color: var(--text-secondary);
}

.main-content {
  padding: 1rem 1.5rem 1.5rem;
  min-height: calc(100vh - 170px);
  transition: padding var(--motion-base), transform var(--motion-base);
}

.main-surface {
  min-height: 100%;
  transition: opacity var(--motion-base), transform var(--motion-base);
}

.footer {
  height: auto;
  padding: 0 1.5rem 1.5rem;
  background: transparent;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  flex-wrap: wrap;
  padding: 1rem 1.25rem;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-soft);
  background: color-mix(in srgb, var(--surface-card) 86%, transparent);
  color: var(--text-secondary);
  box-shadow: var(--shadow-card);
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all var(--motion-base);
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}

@media (max-width: 1200px) {
  .header {
    flex-direction: column;
  }

  .header-right {
    width: 100%;
  }

  .header-toolbar {
    width: 100%;
    justify-content: space-between;
  }
}

@media (max-width: 960px) {
  .layout-container {
    display: block;
  }

  .sidebar {
    width: auto !important;
    min-height: auto;
    padding-bottom: 0;
  }

  .sidebar-menu {
    overflow-x: auto;
  }

  .main-content,
  .header,
  .footer {
    padding-inline: 1rem;
  }

  .header-toolbar {
    flex-wrap: wrap;
  }
}
</style>
