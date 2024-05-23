<template>
  <div>
    <Card class="m-5">
      <div class="flex items-center">
        <h1 class="text-xl">{{ props.name }}</h1>
        <ModalDeleteProject class="ml-auto" @delete-project="handleClickDelete" v-model:isOpen="state.isOpen" :project-name="props.name" :project-id="props.id"></ModalDeleteProject>
      </div>
      <p class="my-5 max-h-32 text-ellipsis overflow-auto">
        {{ props.summary }}
      </p>
      <div>
        <ButtonSecondary @click="handleClickModify" class="mr-2 my-2"
          >Modifier</ButtonSecondary
        >
        <ButtonPrimary @click="handleClickPreferencies">Vos préférences</ButtonPrimary>
      </div>
    </Card>
  </div>
</template>
<script setup>
import { reactive } from "vue";

const props = defineProps(["id", "name", "summary"]);

const state = reactive({
  isOpen: false,
});

const emit = defineEmits(["modifyProject","deleteProject", "handleClickPreferencies"]);

const handleClickModify = () => {
  emit("modifyProject", {name: props.name, summary: props.summary });
};

const handleClickPreferencies = () => {
  emit("handleClickPreferencies", props.id);
};

const handleClickDelete = () => {
  emit("deleteProject",props.id)
}
</script>
