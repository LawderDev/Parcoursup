<template>
  <VueDatePicker
    v-model="state.date"
    :format="format"
    :disabled-dates="disabledDates"
    :disabled="endDateGroup !== undefined && !endDateGroup"
    style="--dp-border-radius:7px;"
  ></VueDatePicker>
</template>

<script setup>
import { ref, watch } from "vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";

const state = reactive({
  date: null,
});

const props = defineProps({
  endDate: Date,
  endDateGroup: Date,
});

const emit = defineEmits(["update:endDate"]);

watch(
  () => state.date,
  (newDate) => {
    emit("update:endDate", newDate);
  }
);

const format = (date) => {
  const day = date.getDate().toString().padStart(2, "0");
  const month = (date.getMonth() + 1).toString().padStart(2, "0");
  const year = date.getFullYear();

  return `${day}/${month}/${year}`;
};

const disabledDates = (date) => {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return (props.endDateGroup && date < props.endDateGroup) || date < today; // Disable dates before today or endDateGroup
};
</script>
