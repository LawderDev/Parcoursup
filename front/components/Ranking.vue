<template>
        <div>
            <h1 class="card-title pb-4 text-neutral">Vos préférences</h1>
            <p class="pb-4 text-accent text-sm">{{ description }}</p>
            <div class="flex">
                <div class="relative top-[27px] opacity-60">
                    <template v-for="(_, index) in items">
                        <div class="flex items-center mr-5 mt-[2px] mb-[2px] text-neutral text-md font-bold">{{ index + 1 }}</div>
                        <div v-if="index !== items.length - 1"
                            class="relative w-[1px] h-8 bg-neutral left-1 top-0">
                        </div>
                    </template>
                </div>
               
                <draggable 
                class="flex-auto"   
                :list="items" 
                group="people" 
                @change="updateItems"
                item-key="id">
                    <template #item="{element}">
                        <div class="flex mt-5 w-full">
                            <div class="flex-auto justify-start btn min-h-2 h-10 rounded-full neumorphism ">
                                <img alt="rankingIcon" src="@/assets/images/rankingIcon.svg"/>
                                <span class="text-xs font-bold flex-auto text-neutral">{{ element.nom }}</span>
                                <Tooltip :content="element.description">?</Tooltip>
                            </div>
                        </div>
                    </template>
                </draggable>
            </div>
        </div>
</template>
  
<script setup>
//items need to be in the form {name: 'Item 1', description: 'Item 1 description'}
defineProps({
    description: String,
    items: Array, 
})

const emits = defineEmits(['update:items'])

const updateItems = (event) => {
    if(!Array.isArray(event) || event.length !== items.length) return
    emits('update:items', event)
}
</script>
  
<style scoped>
</style>
  