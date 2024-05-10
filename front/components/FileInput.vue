<template>
  <div>
    <input
      type="file"
      :accept="props.fileType"
      @change="handleFileChange"
      ref="fileInput"
      class="file-input file-input-primary file-input-bordered file-input-sm md:file-input-md w-full max-w-xs rounded-badge"
    />
  </div>
</template>
<script setup>
const props = defineProps(["fileType", "fileValue"]);
</script>
