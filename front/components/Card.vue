<template>
    <div class="card bg-base-100 shadow-xl" :class="{ 'w-fit': !noFit }">
        <div class="card-body" :class="{ 'w-fit': !noFit }">
           <slot></slot>
        </div>
    </div>
</template>
  
<script setup>
defineProps({
    noFit: Boolean
})
</script>
  
<style scoped>
</style>
  