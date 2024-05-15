<template>
  <div class="ml-6 mr-6 relative">
    <div
      class="btn btn-block relative z-0 h-20 flex justify-start rounded-3xl bg-base-100 border-0 shadow-transparent"
      @click="$emit('handleClick')"
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
    </div>
    <div class="absolute z-10 top-4 right-4">
      <div @click.stop="$emit('delete')">
        <div class="btn btn-square">
            <img alt="delete-svg" src="../public/delete.svg" class="h-6 w-6" />
        </div>
      </div>
    </div>
   
  </div>
</template>

<script setup>
defineProps({
  title: String,
  endDate: String,
});

defineEmits(['delete', 'handleClick'])
</script>

<style scoped></style>
