<template>
  <div ref="tooltipContainer" class="tooltip tooltip-left" :data-tip="content">
    <div class="btn rounded-full min-w-0 min-h-0 w-7 h-6 text-sm">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';

const props = defineProps({
  content: String
});

const tooltipContainer = ref(null);

onMounted(() => {
  if (tooltipContainer.value) {
    const parentWidth = tooltipContainer.value.parentElement.offsetWidth;
    const tooltipWidth = parentWidth * 0.8; // 80% of the parent width
    tooltipContainer.value.style.setProperty('--tooltip-width', `${tooltipWidth}px`);
  }
});
</script>

<style scoped>
.tooltip[data-tip]::before {
  content: attr(data-tip);
  display: block;
  position: absolute;
  width: var(--tooltip-width);
  background-color: #e6e6e6;
  color: rgb(34, 34, 34);
  border-radius: 22px;
  padding: 8px;
  z-index: 999;
  white-space: normal; /* Allow text to wrap */
  text-align: center;  /* Center align the text */
  line-height: 1.4;    /* Adjust line height for better readability */
}

.tooltip:hover[data-tip]::before {
  visibility: visible;
  opacity: 1;
}

@media (max-width: 768px) { /* For medium devices and below */
  .tooltip[data-tip]::before {
    width: calc(var(--tooltip-width) * 0.9); /* Reduce the tooltip width */
  }
}

@media (max-width: 480px) { /* For small devices and below */
  .tooltip[data-tip]::before {
    width: calc(var(--tooltip-width) * 0.8); /* Reduce the tooltip width */
  }
}
</style>
