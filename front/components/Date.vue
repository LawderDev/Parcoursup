<template>
  <VueDatePicker v-model="date"></VueDatePicker>
</template>

<script setup>
import { ref } from "vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";

const today = new Date();
const date = ref(null);

watch(date, (newVal) => {
  if (newVal && newVal < today) {
    // Reset to today's date if selected date is before today
    date.value = today;
  }
}, { immediate: true }); // Validate on initial render

</script>
