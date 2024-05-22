<template>
    <button class="btn btn-ghost">
      <img alt="image-button" :src="src" class="h-6 w-6" />
      <slot></slot>
    </button>
</template>

<script setup>
defineProps({
  src: String,
})
</script>