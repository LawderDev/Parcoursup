<template>
  <div>
    <Modal
    @close="emit('update:isOpen', false)">
      <template v-slot:open-btn>
        <ButtonPlus
          ref="openBtn"
          @click="handleCreateProject"
          class="neumorphism"
        />
        <div id="hidden" class="hidden" ref="openBtn"></div>
      </template>
      <template v-slot:form>
        <div class="flex flex-col items-center">
          <h1 class="text-3xl mt-3">Créer un projet</h1>
          <div class="my-5">
            <h2 class="ml-1 my-5">Nom</h2>
            <input
              type="text"
              v-model="state.name"
              placeholder="Nom du projet..."
              class="input input-bordered w-full max-w-xs"
            />
            <h2 class="ml-1 my-5">Description</h2>
            <textarea
              v-model="state.summary"
              class="textarea textarea-bordered"
              placeholder="Description du projet..."
            ></textarea>
          </div>
        </div>
      </template>
      <template v-slot:action>
        <button ref="openBtn">
          <ButtonPrimary
            @click="editMode ? handleModify : handleSubmit"
            class="flex justify-center"
            v-if="state.name && state.name.length>0"
            >Valider
          </ButtonPrimary>
          <ButtonPrimary
            disabled="disabled"
            class="flex justify-center"
            v-else
            >Valider
          </ButtonPrimary>
        </button>
      </template>
    </Modal>
  </div>
</template>
<script setup>
import { defineEmits, reactive } from "vue";
const openBtn = ref(null);
const closeBtn = ref(null);
const props = defineProps({
  isOpen: Boolean,
  editMode: Boolean,
  name: String,
  summary: String,
});

const state = reactive({
  name: null,
  summary: null,
})

onMounted(() => {
  if(props.editMode){
    state.name = props.name
    state.summary = props.summary
  
  }
  openBtn.value.click();
})
const emit = defineEmits(["submit:project", "update:isOpen", "createProject"]);

const handleSubmit = () => {
  closeBtn.value.click();
  emit("submit:project", {
    name: state.name,
    summary: state.summary,
  });
};
const handleModify = () => {
  closeBtn.value.click();
  emit("modify:project", {
    name: state.name,
    summary: state.summary,
  });
};
const handleCreateProject = () => {
  emit("create:project");
};
watch(
  () => props.isOpen,
  () => {
    if (props.isOpen) {
      console.log("props.isOpen",props.isOpen);
      openBtn.value.click();
    }
  }
);
</script>
