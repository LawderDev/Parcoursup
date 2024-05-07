<template>
    <button class="btn btn-circle bg-base-100">
        <img alt="plus" src="../assets/images/plus.png" class="h-6 w-6"/>
    </button>
</template>

<script setup>
defineProps({
    title: String,
    endDate : String
});
</script>

<style scoped></style>
