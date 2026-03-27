<template>
  <section class="table-container admin-table">
    <slot />
    <div v-if="$slots.pagination" class="pagination-wrapper">
      <slot name="pagination" />
    </div>
  </section>
</template>
