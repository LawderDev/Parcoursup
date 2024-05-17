<template>
  <VueDatePicker
    v-model="state.date"
    :format="format"
  ></VueDatePicker>
</template>

<script setup>
import { ref, watch } from "vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";

const state = reactive({
  date: null,
});

const emit = defineEmits(["date"]);

watch(
  () => state.date,
  (newDate) => {
    emit("date", newDate);
  }
);

const format = (date) => {
  const day = date.getDate().toString().padStart(2, "0");
  const month = (date.getMonth() + 1).toString().padStart(2, "0");
  const year = date.getFullYear();

  return `${day}/${month}/${year}`;
};
</script>
