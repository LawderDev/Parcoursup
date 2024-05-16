<template>
    <div class="btn btn-md bg-base-100 rounded-full text-primary">
      <img alt="image-button" :src="src" class="h-4 w-4" />
      <slot></slot>
    </div>
</template>

<script setup>
defineProps({
  src: String,
})
</script>