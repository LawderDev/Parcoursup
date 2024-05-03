<template>
  <button class="btn btn-xs sm:btn-sm md:btn-md lg:btn-lg btn-outline btn-primary rounded-full">{{title}}</button>
</template>

<script setup>
const props = defineProps({
  title: String
})
</script>

<style scoped>

</style>