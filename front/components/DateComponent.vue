<template>
  <VueDatePicker v-model="selectedDate" :format="format" :disabled-dates="disabledDates" />
</template>

<script setup>
import { ref, watch } from "vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";

const props = defineProps(["selectedDate"]);

const emit  = defineEmits(['newDateSelected']);

const selectedDate = ref(props.selectedDate);

watch(selectedDate, (newDate) => {
  emit("newDateSelected",newDate)
})

const format = (date) => {
  const day = date.getDate().toString().padStart(2, '0');
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const year = date.getFullYear();

  return `${day}/${month}/${year}`;
}
const disabledDates = (date) => {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return date < today;
};



</script>
