<template>
  <div>
    <Toaster :message="toaster.message" :type="toaster.type" :duration="toaster.duration" :is-open="toaster.isOpen"></Toaster>
    <NuxtPage />
  </div>

</template>

<script setup>
import { useToasterStore } from './stores/toaster';

const toaster = useToasterStore();
</script>

<style>
.neumorphism {
  box-shadow:  5px 5px 10px #bebebe,
}        
</style>
