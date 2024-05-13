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
    reader.onload = (e) => {
      emit("fileSelected", e.target.result);
    };

    reader.readAsText(file);
  }
};
</script>
