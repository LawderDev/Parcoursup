<template>
  <input
    type="file"
    class="file-input file-input-primary file-input-bordered file-input-sm md:file-input-md w-full max-w-xs rounded-badge"
    @change="handleFileChange"
    :accept="acceptedTypes"
    ref="fileInput"
  />
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue';

const props = defineProps({
  acceptedTypes: {
    type: String,
    default: ''
  }
});

const emit  = defineEmits(['fileSelected']);

const selectedFile = ref(null);

const handleFileChange = (event) => {
  const file = event.target.files[0];
  selectedFile.value = file;
  emit('fileSelected', file);
};
</script>
