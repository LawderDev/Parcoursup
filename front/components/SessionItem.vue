<template>
  <div class="ml-6 mr-6">
    <button
      class="btn btn-block h-20 flex justify-start rounded-3xl bg-base-100 border-0 shadow-transparent"
    >
      <ImagePlaceHolder>{{ title[0] }}</ImagePlaceHolder>

      <div class="text-left">
        <div class="w-[140px]">
          <div
            class="text-lg w-[40vw] md:w-[70vw] overflow-hidden text-ellipsis whitespace-nowrap"
          >
            {{ title }}
          </div>
          <div class="mt-[2px]">
            {{ endDate }}
          </div>
        </div>
      </div>
      <div class="ml-auto">
        <div class="btn btn-square">
            <img alt="delete-svg" src="../public/delete.svg" class="h-6 w-6" />
        </div>
      </div>
    </button>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  endDate: String,
});
</script>

<style scoped></style>
