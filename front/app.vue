<template>
  <div class="app">
    <Toaster :message="toaster.message" :type="toaster.type" :is-open="toaster.isOpen"></Toaster>
    <NuxtPage />
  </div>

</template>

<script setup>
import { useToasterStore } from './stores/toaster';

const toaster = useToasterStore();
</script>

<style>
.neumorphism {
  box-shadow: 5px 5px 10px #bebebe, -5px -5px 10px #ffffff;
}

.app {
  font-family: "DM-Sans", sans-serif;
  font-optical-sizing: auto;
  font-weight: 200;
  font-style: normal;
}
</style>
