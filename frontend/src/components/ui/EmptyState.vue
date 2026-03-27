<template>
  <div class="empty-state">
    <div class="empty-state-mark">{{ mark }}</div>
    <h3 class="empty-state-title">{{ title }}</h3>
    <p class="empty-state-text">{{ description }}</p>
    <div v-if="$slots.actions" class="empty-state-actions">
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  mark: {
    type: String,
    default: '卷'
  },
  title: {
    type: String,
    default: '暂时没有内容'
  },
  description: {
    type: String,
    default: '相关数据出现后会展示在这里。'
  }
})
</script>

<style scoped>
.empty-state {
  padding: 2rem 1rem;
  text-align: center;
  display: grid;
  gap: 0.75rem;
}

.empty-state-mark {
  width: 3rem;
  height: 3rem;
  margin: 0 auto;
  display: grid;
  place-items: center;
  border-radius: 999px;
  background: color-mix(in srgb, var(--color-accent) 18%, transparent);
  color: var(--color-primary);
  font-family: var(--font-display);
  font-size: 1.25rem;
}

.empty-state-title {
  margin: 0;
  font-family: var(--font-display);
}

.empty-state-text {
  margin: 0;
  color: var(--text-secondary);
}

.empty-state-actions {
  display: flex;
  justify-content: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}
</style>
