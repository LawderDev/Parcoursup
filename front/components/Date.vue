<template>
  <VueDatePicker v-model="state.date" :disabled-dates="disabledDates"></VueDatePicker>
</template>

<script setup>
import { ref, reactive, watch } from "vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";

const state = reactive({
  date: new Date()
});

const disabledDates = (date) => {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return date < today;
};
</script>
