<template>
    <div class="btn btn-md btn-secondary rounded-full text-primary neumorphism">
      <img alt="image-button" :src="src" class="h-6 w-6" />
      <slot></slot>
    </div>
</template>

<script setup>
defineProps({
  src: String,
})
</script>