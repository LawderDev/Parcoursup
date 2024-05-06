<template>
    <div class="ml-6 mr-6 ">
        <button class="btn btn-block h-20 flex justify-start rounded-3xl bg-base-100 border-0 shadow-transparent">
            <ImagePlaceHolder>{{ title[0] }}</ImagePlaceHolder>
            <div class="text-left">
                <div class="text-lg">
                    {{title}}
                </div>
                <div class="mt-[2px]">
                    {{endDate}}
                </div>
            </div>
        </button>
    </div>
</template>

<script setup>
defineProps({
    title: String,
    endDate : String
});
</script>

<style scoped></style>
