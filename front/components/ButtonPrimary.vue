<template>
  <button class="btn btn-sm md:btn-md btn-primary rounded-full">{{title}}</button>
</template>

<script setup>
const props = defineProps({
  title: String
})
</script>

<style scoped>

</style>