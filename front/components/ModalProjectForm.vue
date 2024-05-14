<template>
  <div>
    <Modal
      @handle-submit="editMode ? handleModify : handleSubmit"
      @close="emit('update:isOpen', false)"
    >
      <template v-slot:open-btn>
        <ButtonPlus ref="openBtn" @click="handleCreateProject" class="neumorphism m-4"/>
        <div id="hidden" class="hidden" ref="openBtn"></div>
      </template>
      <template v-slot:form>
        <div class="flex flex-col items-center">
          <h1 class="text-3xl mt-3">Créer un projet</h1>
          <div class="my-5">
            <h2 class="ml-1 my-5">Nom</h2>
            <input
              type="text"
              v-model="props.name"
              placeholder="Nom du projet..."
              class="input input-bordered w-full max-w-xs"
            />
            <h2 class="ml-1 my-5">Description</h2>
            <textarea
              v-model="props.summary"
              class="textarea textarea-bordered"
              placeholder="Description du projet..."
            ></textarea>
          </div>
        </div>
      </template>
    </Modal>
  </div>
</template>
<script setup>
import { defineEmits, reactive } from "vue";
const openBtn = ref(null);
const props = defineProps({
  isOpen: Boolean,
  editMode: Boolean,
  name: String,
  summary: String,
});

const emit = defineEmits(["submit:project", "update:isOpen","createProject"]);

const state = reactive({
  project: {
    name: props.name,
    summary: props.summary,
  },
});

const handleSubmit = () => {
  emit("submit:project", {
    name: props.name,
    summary: props.summary,
  });
};
const handleModify = () => {
  emit("modify:project", {
    name: props.name,
    summary: props.summary,
  });
};
const handleCreateProject = () => {
  emit("create:project")
};
watch(
  () => props.isOpen,
  () => {
    if (props.isOpen) {
      console.log(props.isOpen);
      openBtn.value.click();
    }
  }
);
</script>
