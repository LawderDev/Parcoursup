<template>
    <div class="flex justify-center">
        <ul class="steps">
            <li class="step" :class="{ 'step-primary': i <= nbStepsActive }" v-for="i in nbSteps" :key="i"></li>
        </ul>
    </div>
</template>

<script setup>
defineProps({
    nbSteps: Number,
    nbStepsActive: Number
})
</script>

<style scoped></style>
