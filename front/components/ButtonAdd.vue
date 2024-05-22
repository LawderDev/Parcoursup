<template>
    <div>
        <ImageButton :src="ButtonPlus" class="shadow-md min-h-[2.5rem] h-[2.5rem]" @click="$emit('handleClick')"><slot></slot></ImageButton>
    </div>
</template>

<script setup>
import ButtonPlus from "@/assets/images/plus.png"

defineProps({
    title: String,
    endDate : String
});

defineEmits(['handleClick'])
</script>

<style scoped></style>
