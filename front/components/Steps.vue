<template>
    <div class="flex justify-center">
        <ul class="steps">
            <template v-for="i in nbSteps">
                <li v-if="i <= nbStepsLock || nbStepsLock === 0" class="step" :class="{ 'step-primary': i <= nbStepsActive }"></li>
                <li v-else data-content="✕" class="step"></li>
            </template>
           
        </ul>
    </div>
</template>

<script setup>
defineProps({
    nbSteps: Number,
    nbStepsActive: Number,
    nbStepsLock: Number,
})
</script>

<style scoped></style>
