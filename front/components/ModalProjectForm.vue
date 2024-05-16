<template>
  <div>
    <Modal @close="emit('update:isOpen', false)">
      <template v-slot:open-btn>
        <ButtonPlus @click="handleCreateProject" class="neumorphism" />
        <div id="hidden" class="hidden" ref="openBtn"></div>
      </template>
      <template v-slot:form>
        <div class="flex flex-col items-center">
          <h1 class="text-3xl mt-3">Créer un projet</h1>
          <div class="my-5">
            <h2 class="ml-1 my-5">Nom</h2>
            <input
              type="text"
              :value="props.name"
              @input="$emit('update:name', $event.target.value)"
              placeholder="Nom du projet..."
              class="input input-bordered w-full max-w-xs"
            />
            <h2 class="ml-1 my-5">Description</h2>
            <textarea
              :value="props.summary"
              @input="$emit('update:summary', $event.target.value)"
              class="textarea textarea-bordered"
              placeholder="Description du projet..."
            ></textarea>
          </div>
        </div>
      </template>
      <template v-slot:action>
        <button @click="emit('update:isOpen', false)">
          <ButtonPrimary
            @click="editMode ? handleModify : handleSubmit"
            class="flex justify-center"
            v-if="props.name && props.name.length > 0"
            >Valider
          </ButtonPrimary>
          <ButtonPrimary disabled="disabled" class="flex justify-center" v-else
            >Valider
          </ButtonPrimary>
        </button>
      </template>
    </Modal>
  </div>
</template>
<script setup>
import { defineEmits } from "vue";
const openBtn = ref(null);
const props = defineProps({
  isOpen: Boolean,
  editMode: Boolean,
  name: String,
  summary: String,
});

onMounted(() => {});
const emit = defineEmits([
  "submit:project",
  "update:isOpen",
  "createProject",
  "update:name",
  "update:summary",
]);

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
  emit("create:project");
};
watch(
  () => props.isOpen,
  () => {
    console.log("watcher", props.isOpen);
    if (props.isOpen) {
      console.log("props.isOpen", props.isOpen);
      openBtn.value.click();
    }
  }
);
</script>
