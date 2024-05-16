<template>
  <div>
    <Card class="m-5">
      <div class="flex items-center">
        <h1 class="text-xl">{{ props.name }}</h1>
        <ModalDeleteSession v-model:isOpen="state.isOpen" :session-title="state.selectedSession.title", :session-id="state.selectedSession.id"></ModalDeleteSession>
      </div>
      <p class="my-5 max-h-32 text-ellipsis overflow-auto">
        {{ props.summary }}
      </p>
      <div>
        <ButtonSecondary @click="handleClickModify" class="mr-2 my-2"
          >Modifier</ButtonSecondary
        >
        <ButtonPrimary>Vos préférences</ButtonPrimary>
      </div>
    </Card>
  </div>
</template>
<script setup>
import { reactive } from "vue";
const props = defineProps(["id","name", "summary"]);
const state = reactive({
  isOpen: false,
});

const emit = defineEmits(["modifyProject","deleteProject"]);

const handleClickModify = () => {
  console.log("modifyProfect");
  emit("modifyProject", { name: props.name, summary: props.summary });
};
const handleClickDelete = () => {
  emit("deleteProject",props.id)
}
</script>
