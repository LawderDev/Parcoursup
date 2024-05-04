<template>
    <div>
        <h1 class="card-title pb-4">Votre classement</h1>
        <p class="pb-4">Classez les groupes de projets en fonction de vos préférences</p>
        <draggable 
        v-model="items" 
        group="people" 
        @start="drag=true" 
        @end="drag=false" 
        class="w-[500px]"
        item-key="id">
            <template #item="{element}">
                <div class="alert mt-2 pt-2 pb-2 rounded-full">
                    <img alt="rankingIcon" src="@/assets/images/rankingIcon.svg"/>
                    <span class="flex justify-center items-center w-full">{{ element.name }}</span>
                </div>
            </template>
        </draggable>
    </div>
</template>
  
<script setup>
  let items = ref([
  {
    name: 'Item 1'
  },
  {
    name: 'Item 2'
  },
  {
    name: 'Item 3'
  }
]);
</script>
  
  <style scoped>
  </style>
  