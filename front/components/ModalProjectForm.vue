<template>
  <div>
    <Modal @close="emit('update:isOpen', false)" :disabled="props.sessionState !== 'Grouping'">
      <template v-slot:open-btn>
        <ButtonPlus v-if="props.sessionState === 'Grouping'" @click="handleCreateProject" class="neumorphism"/>
        <ButtonPlus v-else class="neumorphism" disabled/>
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
              class="input input-bordered w-[75vw] md:w-[35vw]"
            />
            <h2 class="ml-1 my-5">Description</h2>
            <textarea
              :value="props.summary"
              @input="$emit('update:summary', $event.target.value)"
              class="textarea textarea-bordered w-[75vw] md:w-[35vw]"
              placeholder="Description du projet..."
            ></textarea>
          </div>
        </div>
      </template>
      <template v-slot:action>
        <button @click="emit('update:isOpen', false)">
          <ButtonPrimary
            @click="handleClickValidate"
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
  id: Number,
  name: String,
  summary: String,
  sessionState: String,
});

const emit = defineEmits([
  "submit:project",
  "update:isOpen",
  "create:project",
  "update:name",
  "update:summary",
  "modify:project",
]);

const handleSubmit = () => {
  emit("submit:project", {
    name: props.name,
    summary: props.summary,
  });
};
const handleModify = () => {
  console.log("heer")
  console.log(props.id)
  console.log(props.name)
  console.log(props.summary)
  emit("modify:project", {
    id: props.id,
    name: props.name,
    summary: props.summary,
  });
};
const handleCreateProject = () => {
  emit("create:project");
};
const handleClickValidate = ()=>{
  if(props.editMode ){
    handleModify()
  }else{
    handleSubmit()
  }
}
watch(
  () => props.isOpen,
  () => {
    if (props.isOpen) {
      openBtn.value.click();
    }
  }
);
</script>
