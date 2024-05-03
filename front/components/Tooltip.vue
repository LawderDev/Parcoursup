<template>
  <div class="tooltip tooltip-right" :data-tip="content">
    <button class="btn rounded-full w-16 h-12 text-2xl"><slot></slot></button>
    
  </div>
</template>

<script setup>
defineProps({
  content: String
})
</script>

<style scoped></style>
