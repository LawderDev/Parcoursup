<template>
  <VueDatePicker v-model="state.date"></VueDatePicker>
</template>

<script setup>
import { ref, reactive } from "vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
  
const state = reactive({
  date: "",
});
  
const today = new Date();

watch(state.date, (newVal) => {
  if (newVal && newVal < today) {
    state.date = today;
  }
}, { immediate: true }); // Validate on initial render

</script>
