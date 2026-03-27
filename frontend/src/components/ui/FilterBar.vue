<template>
  <section class="filter-card">
    <div v-if="title || description" class="filter-bar-header">
      <div>
        <h3 v-if="title" class="section-card-title">{{ title }}</h3>
        <p v-if="description" class="section-meta">{{ description }}</p>
      </div>
      <div v-if="$slots.actions" class="filter-bar-actions">
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
.filter-bar-header {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.filter-bar-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}
</style>
