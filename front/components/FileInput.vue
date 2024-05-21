<template>
  <input
    type="file"
    class="file-input file-input-primary file-input-bordered file-input-m w-full rounded-badge"
    @change="handleFileChange"
    :accept="acceptedTypes"
  />
</template>

<script setup>
import { ref, defineProps, defineEmits } from "vue";
import Papa from 'papaparse';
const emit = defineEmits(["fileSelected"]);

const props = defineProps({
  acceptedTypes: {
    type: String,
    default: "",
  },
});

const state = reactive({
  selectedFile: null,
});

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = () => {
      const csv = reader.result;
      // Parse CSV
      const parsedData = Papa.parse(csv, { header: true, delimiter: ";" });
      emit("fileSelected", parsedData);
    };
    reader.readAsText(file);
  }
};
</script>
