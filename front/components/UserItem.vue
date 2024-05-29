<template>
    <div class="ml-6 mr-6 relative">
      <div
        class="btn btn-block relative z-0 h-24 flex justify-start rounded-3xl bg-base-100 border-0 shadow-transparent"
        @click="$emit('handleClick')"
      >
        <ImagePlaceHolder>{{ name[0] }}</ImagePlaceHolder>
  
        <div class="text-left">
          <div class="w-[190px] flex flex-col gap-1 md:gap-0 pb-1">
            <div
              class="text-lg ml-5 w-[40vw] md:w-[70vw] overflow-hidden text-ellipsis whitespace-nowrap"
            >
              {{ name }} {{ firstname }}
            </div>
          </div>
        </div>
      </div>
      <div class="absolute z-10 top-6 right-4">
        <div @click.stop="$emit('delete')">
          <div class="btn btn-square">
              <img alt="delete-svg" src="../public/delete.svg" class="h-6 w-6" />
          </div>
        </div>
      </div>
     
    </div>
  </template>
  
  <script setup>
  const props = defineProps({
    name: String,
    firstname: String,
  });
  
  defineEmits(['delete','handleClick'])
  </script>
  
  <style scoped></style>
  