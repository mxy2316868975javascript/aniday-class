<template>
  <el-button class="app-button" :type="type" :plain="plain" v-bind="$attrs">
    <slot />
  </el-button>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    default: 'primary'
  },
  plain: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.app-button {
  min-height: 2.8rem;
  padding-inline: 1.15rem;
}
</style>
