<template>
  <div class="relative">
    <img src="../public/profil.svg" alt="profil" />
    <div v-if="lettre" 
      class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-white text-xl uppercase"
    >
      {{  lettre }}
    </div>
  </div>
</template>

<script setup>
const props = defineProps(['nom'])
const lettre = computed(() => props.nom.charAt(0));
</script>
