<template>
  <div class="tooltip tooltip-right" :data-tip="content">
    <button class="btn rounded-full min-w-0 min-h-0 w-7 h-6 text-sm">
      <slot></slot>
    </button>
  </div>
</template>

<script setup>
defineProps({
  content: String
})
</script>

<style scoped></style>
