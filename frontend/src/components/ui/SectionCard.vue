<template>
  <section class="section-card">
    <div v-if="title || $slots.header || $slots.actions" class="section-card-header">
      <div class="section-card-copy">
        <slot name="header">
          <h3 v-if="title" class="section-card-title">{{ title }}</h3>
          <p v-if="description" class="section-meta">{{ description }}</p>
        </slot>
      </div>
      <div v-if="$slots.actions" class="section-card-actions">
        <slot name="actions" />
      </div>
    </div>
    <slot />
  </section>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.section-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1rem;
}

.section-card-copy {
  min-width: 0;
}

.section-card-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}
</style>
