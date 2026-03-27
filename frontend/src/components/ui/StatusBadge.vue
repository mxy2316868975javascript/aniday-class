<template>
  <el-tag :type="type" effect="light" class="status-badge">
    <slot>{{ label }}</slot>
  </el-tag>
</template>

<script setup>
defineProps({
  label: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.status-badge {
  font-weight: 600;
}
</style>
