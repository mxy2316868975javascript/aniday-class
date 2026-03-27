<template>
  <article class="stat-card ui-stat-card" :class="toneClass">
    <div class="ui-stat-copy">
      <p class="stat-label">{{ label }}</p>
      <div class="stat-value">{{ value }}</div>
      <p v-if="meta" class="section-meta">{{ meta }}</p>
    </div>
    <div v-if="$slots.icon" class="ui-stat-icon">
      <slot name="icon" />
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  meta: {
    type: String,
    default: ''
  },
  tone: {
    type: String,
    default: 'primary'
  }
})

const toneClass = computed(() => `ui-stat-card--${props.tone}`)
</script>

<style scoped>
.ui-stat-card {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: flex-start;
}

.ui-stat-copy {
  min-width: 0;
}

.ui-stat-icon {
  width: 2.75rem;
  height: 2.75rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: color-mix(in srgb, currentColor 14%, transparent);
  color: inherit;
  font-size: 1.25rem;
}

.ui-stat-card--primary {
  color: var(--color-primary);
}

.ui-stat-card--success {
  color: var(--color-success);
}

.ui-stat-card--warning {
  color: var(--color-warning);
}

.ui-stat-card--danger {
  color: var(--color-danger);
}

.ui-stat-card :deep(.stat-label),
.ui-stat-card :deep(.section-meta) {
  color: var(--text-secondary) !important;
}

.ui-stat-card :deep(.stat-value) {
  color: currentColor !important;
}
</style>
