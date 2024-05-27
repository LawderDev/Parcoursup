<template>
  <div>
    <Card class="m-5">
      <div class="flex items-center">
        <h1 class="text-xl">{{ props.name }}</h1>
        <ModalDeleteProject class="ml-auto" @delete-project="handleClickDelete" v-model:isOpen="state.isOpen" :project-name="props.name" :project-id="props.id" :disabled="props.sessionState !== 'Grouping'"></ModalDeleteProject>
      </div>
      <p class="my-5 max-h-32 text-ellipsis overflow-auto">
        {{ props.summary }}
      </p>
      <div>
        <ButtonSecondary v-if="props.sessionState === 'Grouping'" @click="handleClickModify" class="mr-2 my-2"
          >Modifier</ButtonSecondary
        >
        <ButtonSecondary v-else @click="handleClickModify" class="mr-2 my-2" disabled>Modifier</ButtonSecondary
        >
        <ButtonPrimary v-if ="props.sessionState === 'Choosing'" @click="handleClickPreferencies">Vos préférences</ButtonPrimary>
        <ButtonPrimary v-else @click="handleClickPreferencies" disabled>Vos préférences</ButtonPrimary>
      </div>
    </Card>
  </div>
</template>
<script setup>
import { reactive } from "vue";

const props = defineProps({
  id: Number,
  name: String,
  summary: String,
  sessionState: String,
});

const state = reactive({
  isOpen: false,
});

const emit = defineEmits(["modifyProject","deleteProject", "handleClickPreferencies"]);

const handleClickModify = () => {
  emit("modifyProject", {id: props.id, name: props.name, summary: props.summary });
};

const handleClickPreferencies = () => {
  emit("handleClickPreferencies", props.id);
};

const handleClickDelete = () => {
  emit("deleteProject",props.id)
}
</script>
