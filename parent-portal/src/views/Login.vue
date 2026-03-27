<template>
  <div class="portal-page parent-login">
    <section class="portal-hero">
      <p class="portal-kicker">Parent Access</p>
      <h1>安心查看孩子的学习进展</h1>
      <p class="hero-copy">通过班主任提供的 8 位家长码，快速绑定孩子，查看成绩、通知与作业。</p>
    </section>

    <main class="login-main">
      <div class="portal-card login-card">
        <div class="login-card-header">
          <div class="seal">家</div>
          <div>
            <p class="portal-kicker portal-muted">Aniday Class Family Portal</p>
            <h2>绑定孩子</h2>
          </div>
        </div>

        <el-form :model="form" :rules="rules" ref="formRef" size="large" class="login-form">
          <el-form-item prop="parentCode">
            <el-input
              v-model="form.parentCode"
              placeholder="请输入8位家长码"
              maxlength="8"
              :prefix-icon="Key"
              @keyup.enter="handleLogin"
            />
          </el-form-item>

          <el-form-item>
            <el-button type="primary" :loading="loading" @click="handleLogin" class="login-btn">
              {{ loading ? '验证中...' : '绑定孩子' }}
            </el-button>
          </el-form-item>
        </el-form>

        <div class="tips">
          <p>请使用班主任提供的 8 位家长码。</p>
          <p>若绑定失败，请联系学校老师重新生成家长码。</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Key } from '@element-plus/icons-vue'
import api from '@/api'

const router = useRouter()
const formRef = ref()
const loading = ref(false)

const form = ref({
  parentCode: ''
})

const rules = {
  parentCode: [
    { required: true, message: '请输入家长码', trigger: 'blur' },
    { min: 8, max: 8, message: '家长码为8位', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  await formRef.value.validate()

  loading.value = true
  try {
    const verifyResult = await api.verifyCode(form.value.parentCode)

    if (verifyResult.valid) {
      localStorage.setItem('parent_code', form.value.parentCode)
      localStorage.setItem('student_name', verifyResult.student_name)
      localStorage.setItem('class_name', verifyResult.class_name)

      ElMessage.success(`绑定成功！欢迎，${verifyResult.student_name}的家长`)

      const student = await api.getStudent(form.value.parentCode)
      localStorage.setItem('student_id', student.student_id)
      localStorage.setItem('class_id', student.class_id)

      router.push('/home')
    } else {
      ElMessage.error(verifyResult.message)
    }
  } catch (error) {
    ElMessage.error(error.detail || error.message || '验证失败，请检查家长码是否正确')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.parent-login {
  display: grid;
  align-content: start;
}

.hero-copy {
  margin-top: 0.65rem;
  max-width: 24rem;
  color: rgba(248, 244, 236, 0.84);
  line-height: 1.7;
}

.login-main {
  padding: 1rem;
  margin-top: -2rem;
}

.login-card {
  padding: 1.2rem;
}

.login-card-header {
  display: flex;
  align-items: center;
  gap: 0.9rem;
  margin-bottom: 1.1rem;
}

.seal {
  width: 3rem;
  height: 3rem;
  display: grid;
  place-items: center;
  border-radius: 1rem;
  background: linear-gradient(145deg, color-mix(in srgb, var(--color-accent) 62%, white 38%) 0%, color-mix(in srgb, var(--color-primary) 78%, black 22%) 100%);
  color: var(--text-inverse);
  font-family: var(--portal-font-display);
  font-size: 1.2rem;
}

.login-card-header h2 {
  margin: 0.2rem 0 0;
  font-family: var(--portal-font-display);
}

.login-btn {
  width: 100%;
  min-height: 3rem;
}

.tips {
  display: grid;
  gap: 0.45rem;
  color: var(--text-secondary);
  font-size: 0.92rem;
  line-height: 1.7;
}

.tips p {
  margin: 0;
}
</style>
